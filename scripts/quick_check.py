import time
from taxicab.search import SearchConfig, sweep, multi_representation_summary
from taxicab.signs import SignRegime


def main() -> None:
    print("Starting sweep up to N = 1,000,000...")
    start = time.time()
    
    # Configure the sweep to use positive a, b pairs and 4 workers
    config = SearchConfig(n_max=1_000_000, regime=SignRegime.POSITIVE, n_workers=4)
    df = sweep(config)
    
    elapsed = time.time() - start
    print(f"Sweep of N<=10^6 took {elapsed:.2f}s, found {len(df)} representations.")
    
    summary = multi_representation_summary(df)
    print(f"{len(summary)} values of N have >= 2 representations.")
    print("\nTop 10 multi-representation N values:")
    print(summary.head(10))


# Crucial Windows guard to prevent recursive subprocess spawning
if __name__ == "__main__":
    main()
