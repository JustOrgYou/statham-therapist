import http from "k6/http";
import { sleep } from "k6";

export const options = {
  cloud: {
    distribution: {
      "amazon:us:ashburn": { loadZone: "amazon:us:ashburn", percent: 100 },
    },
    apm: [],
  },
  thresholds: {
    http_req_duration: ["p(95)<300", "p(99)<300"],
  },
};

export default function () {
  http.get("https://statham.ebo.sh");

  http.get("https://statham.ebo.sh/Favorites");

  sleep(1);
}
