#!/usr/bin/env python3

"""
DeFi Alpha Hunter v2 - Example Usage

This script demonstrates how to use the DeFi Alpha Hunter system.
"""

from defi_alpha_hunter import Hunter

def main():
    # Initialize the hunter with config and memory
    hunter = Hunter(
        config_path="config.json",
        db_path="memory.db"
    )
    
    # Run the analysis
    result = hunter.run()
    
    # Print the portfolio allocation
    print("\n=== Portfolio Allocation ===")
    if result.get("allocation"):
        for token, weight in result["allocation"].items():
            print(f"{token}: {weight:.2%}")
    else:
        print("No allocation generated")
    
    # Print summary
    summary = result.get("summary", {})
    print(f"\nTotal signals: {summary.get('total_signals', 0)}")
    print(f"Bullish: {summary.get('bullish_signals', 0)}")
    print(f"Bearish: {summary.get('bearish_signals', 0)}")
    
    # Save output to file
    output_path = "output/results.json"
    hunter.save_output(output_path)
    print(f"\nFull report saved to {output_path}")

if __name__ == "__main__":
    main()