#!/usr/bin/env python3
"""
Langfuse Evaluation Guide - How to leverage tagged and scored traces
"""
import os
from dotenv import load_dotenv
from langfuse import Langfuse
from collections import Counter, defaultdict
import json

def langfuse_evaluation_workflows():
    """Demonstrate key workflows for using tagged/scored traces in Langfuse"""
    load_dotenv()

    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )

    print("🎯 LANGFUSE EVALUATION WORKFLOWS")
    print("="*60)

    # 1. Get all traces with tags and scores
    traces = langfuse.api.trace.list().data
    print(f"📊 Total traces available: {len(traces)}")

    # 2. WORKFLOW 1: Tag-Based Filtering and Analysis
    print(f"\n🏷️  WORKFLOW 1: TAG-BASED ANALYSIS")
    print("-" * 40)

    # Group traces by tags
    tag_groups = defaultdict(list)
    all_tags = []

    for trace in traces:
        if trace.tags:
            all_tags.extend(trace.tags)
            for tag in trace.tags:
                tag_groups[tag].append(trace)

    # Show tag distribution
    tag_counts = Counter(all_tags)
    print("Tag Distribution:")
    for tag, count in tag_counts.most_common():
        print(f"  {tag}: {count} traces")

    # 3. WORKFLOW 2: False Positive Analysis
    print(f"\n🚨 WORKFLOW 2: FALSE POSITIVE ANALYSIS")
    print("-" * 40)

    fp_traces = []
    for tag, trace_list in tag_groups.items():
        if tag.startswith('fp_'):
            fp_traces.extend(trace_list)
            print(f"\n{tag} ({len(trace_list)} cases):")

            # Calculate cost impact of false positives
            total_cost = sum(getattr(trace, 'total_cost', 0) or 0 for trace in trace_list)
            avg_latency = sum(getattr(trace, 'latency', 0) or 0 for trace in trace_list) / len(trace_list) if trace_list else 0

            print(f"  Cost Impact: ${total_cost:.4f}")
            print(f"  Avg Latency: {avg_latency:.2f}ms")

    print(f"\n📈 FALSE POSITIVE SUMMARY:")
    print(f"  Total FP traces: {len(fp_traces)}")
    print(f"  FP Rate: {len(fp_traces)/len(traces)*100:.1f}%")

    # 4. WORKFLOW 3: Score-Based Evaluation
    print(f"\n📊 WORKFLOW 3: SCORE-BASED EVALUATION")
    print("-" * 40)

    # Analyze scores if available
    scored_traces = [trace for trace in traces if hasattr(trace, 'scores') and trace.scores]
    print(f"Traces with scores: {len(scored_traces)}")

    if scored_traces:
        # Group by score types
        score_types = set()
        for trace in scored_traces:
            for score in trace.scores:
                score_types.add(score.name)

        print(f"Score types found: {', '.join(score_types)}")

        # Analyze each score type
        for score_type in score_types:
            values = []
            for trace in scored_traces:
                for score in trace.scores:
                    if score.name == score_type:
                        values.append(score.value)

            if values:
                avg_score = sum(values) / len(values)
                print(f"  {score_type}: avg={avg_score:.2f}, count={len(values)}")

    # 5. WORKFLOW 4: A/B Testing Setup
    print(f"\n🧪 WORKFLOW 4: A/B TESTING FRAMEWORK")
    print("-" * 40)

    print("Setting up A/B tests with your annotated data:")
    print("1. Use tags to identify problem areas (e.g., fp_severity_inflation)")
    print("2. Create new prompts targeting those issues")
    print("3. Test new prompts on the same content")
    print("4. Compare results using Langfuse dashboard")

    # Example A/B test structure
    ab_test_example = {
        "name": "severity_calibration_test",
        "baseline_prompt": "current_prompt_v1",
        "test_prompt": "severity_calibrated_v2",
        "evaluation_criteria": [
            "fp_severity_inflation reduction",
            "maintain accuracy on real violations",
            "cost efficiency"
        ],
        "test_cases": [
            "All traces tagged with fp_severity_inflation",
            "Random sample of accurate_violation traces",
            "Borderline cases"
        ]
    }

    print(f"\nExample A/B Test Structure:")
    print(json.dumps(ab_test_example, indent=2))

    # 6. WORKFLOW 5: Automated Evaluation Pipeline
    print(f"\n🤖 WORKFLOW 5: AUTOMATED EVALUATION")
    print("-" * 40)

    print("Build automated evaluation based on your manual annotations:")
    print("1. Export your tagged examples as ground truth dataset")
    print("2. Create evaluation functions for each tag category")
    print("3. Set up automated scoring for new traces")
    print("4. Monitor for drift in false positive rates")

    # 7. WORKFLOW 6: Dashboard Filtering Tips
    print(f"\n📱 WORKFLOW 6: DASHBOARD ANALYSIS TIPS")
    print("-" * 40)

    dashboard_tips = [
        "Filter by tags in dashboard to focus on specific issues",
        "Use date ranges to track improvement over time",
        "Group by user_id to identify problematic accounts",
        "Sort by cost to find expensive false positives",
        "Use latency filters to optimize performance",
        "Export filtered data for deeper analysis"
    ]

    for i, tip in enumerate(dashboard_tips, 1):
        print(f"{i}. {tip}")

    # 8. Generate Action Plan
    print(f"\n🎯 RECOMMENDED NEXT STEPS")
    print("-" * 40)

    next_steps = [
        f"Focus on 'fp_severity_inflation' (6 cases) - biggest ROI",
        f"A/B test severity calibration prompt improvements",
        f"Set up automated monitoring for FP rate > 30%",
        f"Export all fp_ tagged traces for training data",
        f"Create evaluation dataset from accurate_ tagged traces",
        f"Implement cost tracking for false positive impact"
    ]

    for i, step in enumerate(next_steps, 1):
        print(f"{i}. {step}")

    return {
        'tag_distribution': tag_counts,
        'fp_rate': len(fp_traces)/len(traces)*100,
        'total_traces': len(traces),
        'scored_traces': len(scored_traces)
    }

def export_tagged_traces_for_evaluation():
    """Export tagged traces as evaluation dataset"""
    load_dotenv()

    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )

    traces = langfuse.api.trace.list().data

    # Group by evaluation type
    evaluation_dataset = {
        'false_positives': [],
        'true_positives': [],
        'accurate_cases': [],
        'borderline_cases': []
    }

    for trace in traces:
        if trace.tags:
            trace_data = {
                'trace_id': trace.id,
                'input': trace.input,
                'output': trace.output,
                'tags': trace.tags,
                'timestamp': str(trace.timestamp),
                'cost': getattr(trace, 'total_cost', 0)
            }

            # Categorize based on tags
            if any(tag.startswith('fp_') for tag in trace.tags):
                evaluation_dataset['false_positives'].append(trace_data)
            elif any(tag.startswith('accurate_violation') for tag in trace.tags):
                evaluation_dataset['true_positives'].append(trace_data)
            elif any(tag.startswith('accurate_appropriate') for tag in trace.tags):
                evaluation_dataset['accurate_cases'].append(trace_data)
            elif any(tag.startswith('accurate_borderline') for tag in trace.tags):
                evaluation_dataset['borderline_cases'].append(trace_data)

    # Save to file
    with open('langfuse_evaluation_dataset.json', 'w') as f:
        json.dump(evaluation_dataset, f, indent=2)

    print(f"📁 Exported evaluation dataset:")
    for category, data in evaluation_dataset.items():
        print(f"  {category}: {len(data)} traces")

def create_ab_test_framework():
    """Create framework for A/B testing prompts using tagged data"""

    ab_test_code = """
# A/B Testing Framework for Prompt Optimization

def run_ab_test(test_name, baseline_prompt, test_prompt, evaluation_traces):
    '''Run A/B test comparing two prompts on evaluation data'''

    results = {
        'test_name': test_name,
        'baseline': {'fp_count': 0, 'accuracy': 0, 'cost': 0},
        'variant': {'fp_count': 0, 'accuracy': 0, 'cost': 0}
    }

    # Test both prompts on the same evaluation data
    for trace_data in evaluation_traces:
        # Run baseline
        baseline_result = moderate_content(trace_data['content'], baseline_prompt)

        # Run variant
        variant_result = moderate_content(trace_data['content'], test_prompt)

        # Score results against ground truth
        baseline_score = evaluate_against_ground_truth(baseline_result, trace_data['expected'])
        variant_score = evaluate_against_ground_truth(variant_result, trace_data['expected'])

        # Track metrics
        results['baseline']['accuracy'] += baseline_score['accuracy']
        results['variant']['accuracy'] += variant_score['accuracy']

        if baseline_score['false_positive']:
            results['baseline']['fp_count'] += 1
        if variant_score['false_positive']:
            results['variant']['fp_count'] += 1

    return results

# Example usage:
ab_test_results = run_ab_test(
    'severity_calibration',
    baseline_prompt='current_prompt',
    test_prompt='severity_calibrated_prompt',
    evaluation_traces=fp_severity_inflation_cases
)
"""

    print("🧪 A/B TESTING FRAMEWORK")
    print("=" * 40)
    print(ab_test_code)

if __name__ == "__main__":
    print("Running Langfuse Evaluation Workflows...")
    results = langfuse_evaluation_workflows()

    print(f"\n" + "="*60)
    print("EXPORT EVALUATION DATA")
    print("="*60)
    export_tagged_traces_for_evaluation()

    print(f"\n" + "="*60)
    print("A/B TESTING FRAMEWORK")
    print("="*60)
    create_ab_test_framework()