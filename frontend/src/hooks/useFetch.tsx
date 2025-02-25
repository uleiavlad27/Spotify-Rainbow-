import { useState, useEffect } from "react";

/**
 * A simple custom hook that fetches data from the given URL.
 * @param url The resource URL to fetch.
 * @returns An object with { data, loading, error }.
 */
function useFetch<T>(url: string): { data: T | null; loading: boolean; error: Error | null } {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json() as Promise<T>;
      })
      .then((jsonData) => {
        if (isMounted) {
          setData(jsonData);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err as Error);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [url]);

  return { data, loading, error };
}

export default useFetch;
