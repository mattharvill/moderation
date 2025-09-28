#!/usr/bin/env python3
"""
Langfuse Pattern Analyzer - Pull tagged traces and identify optimization opportunities
"""
import os
from dotenv import load_dotenv
from langfuse import Langfuse
from collections import Counter
import json

def analyze_langfuse_patterns():
    """Analyze tagged traces from Langfuse to identify prompt optimization opportunities"""
    load_dotenv()

    # Initialize Langfuse client
    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )

    print("🔍 Fetching traces from Langfuse...")

    # Get all traces using the API client
    try:
        # Method 1: Try the correct API endpoint
        traces_response = langfuse.api.trace.list()
        trace_list = traces_response.data if hasattr(traces_response, 'data') else []
        print(f"✅ Successfully fetched traces via API")
    except Exception as e:
        print(f"Method 1 failed: {e}")
        try:
            # Method 2: Try direct traces access
            traces_response = langfuse.api.traces.list()
            trace_list = traces_response.data if hasattr(traces_response, 'data') else []
            print(f"✅ Successfully fetched traces via traces.list()")
        except Exception as e2:
            print(f"Method 2 failed: {e2}")
            try:
                # Method 3: Check the API structure
                print("Available API methods:")
                api_methods = [method for method in dir(langfuse.api) if not method.startswith('_')]
                for method in api_methods:
                    print(f"  - langfuse.api.{method}")

                # Try to find the correct traces endpoint
                if hasattr(langfuse.api, 'trace'):
                    trace_api = langfuse.api.trace
                    trace_methods = [method for method in dir(trace_api) if not method.startswith('_')]
                    print(f"\nTrace API methods:")
                    for method in trace_methods:
                        print(f"  - langfuse.api.trace.{method}")

                trace_list = []
                print("⚠️  Could not fetch traces. Please check API documentation.")
            except Exception as e3:
                print(f"Method 3 failed: {e3}")
                trace_list = []

    print(f"📊 Found {len(trace_list)} traces")

    # Debug: Print first trace structure and content
    if trace_list:
        print(f"\n🔍 First trace structure:")
        first_trace = trace_list[0]
        if hasattr(first_trace, '__dict__'):
            print(f"Trace attributes: {list(first_trace.__dict__.keys())}")
        elif isinstance(first_trace, dict):
            print(f"Trace keys: {list(first_trace.keys())}")
        else:
            print(f"Trace methods: {[attr for attr in dir(first_trace) if not attr.startswith('_')]}")

        # Debug: Show actual input content structure
        if hasattr(first_trace, 'input') and first_trace.input:
            print(f"\n🔍 Sample input content (first 1000 chars):")
            input_sample = str(first_trace.input)[:1000]
            print(f"'{input_sample}...'")

        # Debug: Show actual output content structure
        if hasattr(first_trace, 'output') and first_trace.output:
            print(f"\n🔍 Sample output content (first 500 chars):")
            output_sample = str(first_trace.output)[:500]
            print(f"'{output_sample}...'")

        # Debug: Show tags
        if hasattr(first_trace, 'tags') and first_trace.tags:
            print(f"\n🔍 Sample tags: {first_trace.tags}")

        print(f"\n{'-'*60}")

    # Analyze tags
    all_tags = []
    tag_examples = {}

    for trace in trace_list:
        # Get tags from trace - TraceWithDetails objects have direct attributes
        if hasattr(trace, 'tags') and trace.tags:
            all_tags.extend(trace.tags)
            for tag in trace.tags:
                if tag not in tag_examples:
                    tag_examples[tag] = []

                # Get trace attributes directly
                trace_id = getattr(trace, 'id', 'unknown')
                trace_input = getattr(trace, 'input', None)
                trace_output = getattr(trace, 'output', None)

                # Safely truncate strings
                input_text = str(trace_input)[:100] if trace_input else None
                output_text = str(trace_output)[:100] if trace_output else None

                # Try to extract actual content from input or output
                extracted_content = extract_content_from_input(trace_input)
                if extracted_content == str(trace_input)[:100] + "...":
                    # If input extraction failed, try output
                    extracted_content = extract_content_from_output(trace_output)

                tag_examples[tag].append({
                    'trace_id': trace_id,
                    'input': input_text,
                    'output': output_text,
                    'extracted_content': extracted_content
                })

    # Count tag frequency
    tag_counts = Counter(all_tags)

    print(f"\n{'='*60}")
    print("TAG FREQUENCY ANALYSIS")
    print(f"{'='*60}")

    for tag, count in tag_counts.most_common():
        print(f"{tag}: {count} traces")

    print(f"\n{'='*60}")
    print("PATTERN ANALYSIS BY TAG")
    print(f"{'='*60}")

    # Analyze top problematic patterns
    fp_tags = [tag for tag in tag_counts.keys() if tag.startswith('fp_')]
    fn_tags = [tag for tag in tag_counts.keys() if tag.startswith('fn_')]

    if fp_tags:
        print(f"\n🚨 FALSE POSITIVE PATTERNS:")
        for tag in sorted(fp_tags, key=lambda x: tag_counts[x], reverse=True):
            print(f"\n{tag} ({tag_counts[tag]} cases):")
            for example in tag_examples[tag][:2]:  # Show top 2 examples
                content = example.get('extracted_content', 'Content not extracted')
                print(f"  - \"{content}\"")

    if fn_tags:
        print(f"\n⚠️  FALSE NEGATIVE PATTERNS:")
        for tag in sorted(fn_tags, key=lambda x: tag_counts[x], reverse=True):
            print(f"\n{tag} ({tag_counts[tag]} cases):")
            for example in tag_examples[tag][:2]:  # Show top 2 examples
                content = example.get('extracted_content', 'Content not extracted')
                print(f"  - \"{content}\"")

    # Generate optimization recommendations
    print(f"\n{'='*60}")
    print("OPTIMIZATION RECOMMENDATIONS")
    print(f"{'='*60}")

    recommendations = generate_recommendations(tag_counts)
    for rec in recommendations:
        print(f"🎯 {rec}")

    return {
        'tag_counts': tag_counts,
        'tag_examples': tag_examples,
        'recommendations': recommendations
    }

def extract_content_from_input(input_text):
    """Extract the actual content being moderated from the verbose prompt"""
    if not input_text:
        return "No input found"

    # Convert to string if it's not already
    input_str = str(input_text)

    # First, try to extract from the message structure
    import re

    # Look for quoted content patterns that indicate the actual user message
    patterns = [
        r'"([^"]*(?:hot|cute|beautiful|contact|number|phone|address|hookup|sexy|date|meet)[^"]*)"',  # Content with dating keywords
        r'"([^"]{10,80})"',  # Any quoted content between 10-80 chars (likely user messages)
        r"Content to analyze:\s*['\"]([^'\"]+)['\"]",  # Direct content extraction
        r"Message to moderate:\s*['\"]([^'\"]+)['\"]",
        r"User message:\s*['\"]([^'\"]+)['\"]",
        r"analyze this message:\s*['\"]([^'\"]+)['\"]",
        r"following message:\s*['\"]([^'\"]+)['\"]",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, input_str, re.IGNORECASE)
        for match in matches:
            # Filter out system instructions and keep likely user content
            if not any(skip_word in match.lower() for skip_word in [
                'you are an ai', 'follow this', 'step', 'analyze', 'content moderator',
                'hinge dating app', 'violation', 'score', 'reasoning'
            ]):
                if len(match.strip()) > 5:  # Must be at least 5 characters
                    return match.strip()[:100] + ("..." if len(match) > 100 else "")

    # Try to find content after specific indicators
    content_indicators = [
        "Content to analyze:",
        "Message to moderate:",
        "User message:",
        "analyze this message:",
        "following message:",
        "content:"
    ]

    for indicator in content_indicators:
        if indicator.lower() in input_str.lower():
            # Find the content after the indicator
            idx = input_str.lower().find(indicator.lower())
            after_indicator = input_str[idx + len(indicator):].strip()

            # Extract quoted content or content until a newline/end
            quote_match = re.search(r'["\']([^"\']+)["\']', after_indicator)
            if quote_match:
                content = quote_match.group(1).strip()
                if len(content) > 5:
                    return content[:100] + ("..." if len(content) > 100 else "")

    # Fallback: Look for any quoted strings that seem like user messages
    all_quotes = re.findall(r'["\']([^"\']{10,100})["\']', input_str)
    for quote in all_quotes:
        if not any(skip_word in quote.lower() for skip_word in [
            'you are', 'follow', 'step', 'analyze', 'moderator', 'violation'
        ]):
            return quote[:100] + ("..." if len(quote) > 100 else "")

    # Final fallback: first 100 characters
    return input_str[:100] + "..."

def extract_content_from_output(output_text):
    """Extract the actual content being moderated from the AI's response"""
    if not output_text:
        return "No output found"

    import re
    output_str = str(output_text)

    # Look for quoted content in the AI response
    patterns = [
        r'"([^"]{10,100})"',  # Any quoted content 10-100 chars
        r"message:\s*['\"]([^'\"]+)['\"]",  # After "message:"
        r"content:\s*['\"]([^'\"]+)['\"]",  # After "content:"
        r"text:\s*['\"]([^'\"]+)['\"]",     # After "text:"
        r"says:\s*['\"]([^'\"]+)['\"]",     # After "says:"
        r"wrote:\s*['\"]([^'\"]+)['\"]",    # After "wrote:"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, output_str, re.IGNORECASE)
        for match in matches:
            # Filter out AI response artifacts
            if not any(skip_word in match.lower() for skip_word in [
                'step', 'analysis', 'assessment', 'violation', 'score', 'recommend',
                'context', 'harm', 'appropriate', 'dating app', 'user safety'
            ]):
                if len(match.strip()) > 8:  # Must be at least 8 characters
                    return match.strip()[:100] + ("..." if len(match) > 100 else "")

    return "Could not extract content"

def generate_recommendations(tag_counts):
    """Generate specific prompt optimization recommendations based on tag patterns"""
    recommendations = []

    # False positive recommendations
    if tag_counts.get('fp_compliment', 0) > 2:
        recommendations.append("Add explicit guidance: 'Respectful compliments are APPROPRIATE for dating apps'")

    if tag_counts.get('fp_date_request', 0) > 2:
        recommendations.append("Clarify: 'Date requests are the PURPOSE of dating apps - only flag if pressuring/demanding'")

    if tag_counts.get('fp_phone_number_request', 0) > 2:
        recommendations.append("Distinguish: 'Phone number requests after conversation vs immediate demands'")

    if tag_counts.get('fp_severity_inflation', 0) > 2:
        recommendations.append("Add severity calibration: 'Score 7+ only for clear violations, not borderline cases'")

    # False negative recommendations
    if tag_counts.get('fn_harassment_missed', 0) > 1:
        recommendations.append("Strengthen harassment detection: 'Identify aggressive language patterns'")

    if tag_counts.get('fn_boundary_violation_missed', 0) > 1:
        recommendations.append("Improve boundary detection: 'Flag premature personal information requests'")

    return recommendations

if __name__ == "__main__":
    analyze_langfuse_patterns()