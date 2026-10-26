import pathlib

import httpx

env = {}
env_path = pathlib.Path(__file__).resolve().parents[1] / ".env"
for line in env_path.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

url = env["SUPABASE_URL"].rstrip("/")
for role in ("SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_ANON_KEY"):
    key = env[role]
    h = {"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json"}
    print("=====", role)
    r = httpx.post(
        url + "/rest/v1/rpc/get_nearby_pois",
        headers=h,
        json={"user_lng": -70.6483, "user_lat": -33.4569, "radius_meters": 5000000},
        timeout=20,
    )
    print("RPC", r.status_code, r.text[:1200])
    s = httpx.get(url + "/rest/v1/pois?select=id&limit=1", headers=h, timeout=20)
    print("TABLE", s.status_code, s.text[:300])
