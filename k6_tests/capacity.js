import { sleep } from "k6";
import http from "k6/http";

export const options = {
  ext: {
    loadimpact: {
      projectID: 3694139,
      name: "statham-therapist",
    },
  },
  cloud: {
    distribution: {
      "amazon:us:ashburn": { loadZone: "amazon:us:ashburn", percent: 100 },
    },
    apm: [],
  },
  scenarios: {
    capacity: {
      executor: "ramping-vus",
      gracefulStop: "30s",
      stages: [
        { target: 5, duration: "30s" },
        { target: 5, duration: "30s" },
        { target: 0, duration: "30s" },
      ],
      gracefulRampDown: "30s",
      exec: "capacity",
    },
  },
  thresholds: {
    http_req_duration: ["p(95)<300", "p(99)<300"],
  },
};

export function capacity() {
  http.get("https://statham.ebo.sh");

  http.get("https://statham.ebo.sh/Favorites");

  sleep(1);
}
