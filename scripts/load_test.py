import concurrent.futures
import time
import requests


URL = "http://127.0.0.1:8000/api/v1/screener?min_roe=15"


def call_api(request_number):
    start = time.perf_counter()

    try:
        response = requests.get(URL, timeout=10)

        elapsed = time.perf_counter() - start

        return {
            "request": request_number,
            "status": response.status_code,
            "time": elapsed,
            "success": response.status_code == 200,
        }

    except Exception as exc:
        return {
            "request": request_number,
            "status": "ERROR",
            "time": None,
            "success": False,
            "error": str(exc),
        }


def main():

    print("=" * 70)
    print("SPRINT 6 - API LOAD TEST")
    print("=" * 70)

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=10
    ) as executor:

        results = list(
            executor.map(
                call_api,
                range(1, 11)
            )
        )

    total_time = time.perf_counter() - start

    print("\nIndividual requests:")

    for result in results:
        print(result)

    successful = sum(
        result["success"]
        for result in results
    )

    response_times = [
        result["time"]
        for result in results
        if result["time"] is not None
    ]

    print("\n" + "=" * 70)
    print(f"Successful requests : {successful}/10")
    print(f"Total time          : {total_time:.3f} seconds")

    if response_times:
        print(
            f"Average response    : "
            f"{sum(response_times) / len(response_times):.3f} seconds"
        )

        print(
            f"Maximum response    : "
            f"{max(response_times):.3f} seconds"
        )

    print("=" * 70)

    if successful == 10 and total_time < 10:
        print("LOAD TEST: PASS")
    else:
        print("LOAD TEST: FAIL")


if __name__ == "__main__":
    main()