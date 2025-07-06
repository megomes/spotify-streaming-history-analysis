"""
Command Line Interface for Spotify Analysis Sleep Apnea Project.
"""

import argparse
import sys
from pathlib import Path
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from spotify_analysis.core.data_loader import load_spotify_data
    from spotify_analysis.core.data_transformer import transform_data
    from spotify_analysis.core.pattern_analyzer import analyze_patterns
except ImportError:
    print("Error: Could not import spotify_analysis modules.")
    print("Make sure you have installed the package correctly.")
    sys.exit(1)


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Spotify Analysis Sleep Apnea - Command Line Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  spotify-analysis load --path "Spotify Extended Streaming History"
  spotify-analysis transform --input data.csv --output transformed.csv
  spotify-analysis analyze --input transformed.csv --output results.json
  spotify-analysis full --path "Spotify Extended Streaming History" --output results/
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load Spotify data')
    load_parser.add_argument(
        '--path',
        type=str,
        default='Spotify Extended Streaming History',
        help='Path to directory containing Spotify JSON files'
    )
    load_parser.add_argument(
        '--output',
        type=str,
        help='Output file for loaded data (CSV format)'
    )
    
    # Transform command
    transform_parser = subparsers.add_parser('transform', help='Transform loaded data')
    transform_parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input CSV file with loaded data'
    )
    transform_parser.add_argument(
        '--output',
        type=str,
        help='Output file for transformed data (CSV format)'
    )
    transform_parser.add_argument(
        '--steps',
        nargs='+',
        default=['process_timestamps', 'process_duration', 'clean_duplicates'],
        help='Transformation steps to apply'
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze transformed data')
    analyze_parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input CSV file with transformed data'
    )
    analyze_parser.add_argument(
        '--output',
        type=str,
        help='Output directory for analysis results'
    )
    
    # Full pipeline command
    full_parser = subparsers.add_parser('full', help='Run full analysis pipeline')
    full_parser.add_argument(
        '--path',
        type=str,
        default='Spotify Extended Streaming History',
        help='Path to directory containing Spotify JSON files'
    )
    full_parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='Output directory for all results'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'load':
            run_load(args, logger)
        elif args.command == 'transform':
            run_transform(args, logger)
        elif args.command == 'analyze':
            run_analyze(args, logger)
        elif args.command == 'full':
            run_full_pipeline(args, logger)
        else:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def run_load(args, logger):
    """Run data loading."""
    logger.info(f"Loading data from: {args.path}")
    
    try:
        data = load_spotify_data(args.path)
        logger.info(f"Successfully loaded {len(data)} records")
        
        if args.output:
            data.to_csv(args.output, index=False)
            logger.info(f"Data saved to: {args.output}")
        else:
            print(f"Loaded {len(data)} records")
            print(f"Columns: {list(data.columns)}")
            
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise


def run_transform(args, logger):
    """Run data transformation."""
    logger.info(f"Transforming data from: {args.input}")
    
    try:
        import pandas as pd
        data = pd.read_csv(args.input)
        
        transformed_data = transform_data(data, steps=args.steps)
        logger.info(f"Successfully transformed {len(transformed_data)} records")
        
        if args.output:
            transformed_data.to_csv(args.output, index=False)
            logger.info(f"Transformed data saved to: {args.output}")
        else:
            print(f"Transformed {len(transformed_data)} records")
            print(f"New columns: {list(set(transformed_data.columns) - set(data.columns))}")
            
    except Exception as e:
        logger.error(f"Failed to transform data: {e}")
        raise


def run_analyze(args, logger):
    """Run pattern analysis."""
    logger.info(f"Analyzing data from: {args.input}")
    
    try:
        import pandas as pd
        data = pd.read_csv(args.input)
        
        results = analyze_patterns(data)
        logger.info("Analysis completed successfully")
        
        if args.output:
            import json
            output_path = Path(args.output)
            output_path.mkdir(exist_ok=True)
            
            with open(output_path / "analysis_results.json", "w") as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to: {args.output}")
        else:
            print("Analysis completed")
            print(f"Analysis types: {list(results.keys())}")
            
    except Exception as e:
        logger.error(f"Failed to analyze data: {e}")
        raise


def run_full_pipeline(args, logger):
    """Run the full analysis pipeline."""
    logger.info("Starting full analysis pipeline")
    
    try:
        # Load data
        logger.info("Step 1: Loading data")
        data = load_spotify_data(args.path)
        logger.info(f"Loaded {len(data)} records")
        
        # Transform data
        logger.info("Step 2: Transforming data")
        transformed_data = transform_data(data)
        logger.info(f"Transformed {len(transformed_data)} records")
        
        # Analyze patterns
        logger.info("Step 3: Analyzing patterns")
        results = analyze_patterns(transformed_data)
        logger.info("Analysis completed")
        
        # Save results
        output_path = Path(args.output)
        output_path.mkdir(exist_ok=True)
        
        # Save transformed data
        transformed_data.to_csv(output_path / "transformed_data.csv", index=False)
        
        # Save analysis results
        import json
        with open(output_path / "analysis_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save summary
        import pandas as pd
        summary = {
            "total_records": len(data),
            "transformed_records": len(transformed_data),
            "analysis_timestamp": str(pd.Timestamp.now()),
            "output_directory": str(output_path.absolute())
        }
        
        with open(output_path / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Full pipeline completed. Results saved to: {output_path}")
        print(f"✅ Analysis completed! Results saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main() 