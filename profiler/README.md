# Hashing Performance Profiler
The goal of this is to test the speed with which python can calculate hashes by reading the file in by chunk once for all algorithms versus once per algorithm. One would think that calculating the hashes simultaneously is going to be faster, but by how much?

# Running
Open up profile.py and change init to specify the number of rounds you want to run (or remove altogether).

Then run:
`python profile.py`

# Results
Results will be highly dependent on a lot of different variables, including your file system and cpu. My average results over five runs looks like this:

```json
{
  "rounds": 5,
  "individual_time": 323.71922731399536,
  "bulk_time": 313.8499493598938,
  "savings": 9.869277954101562,
  "percent_savings": "3.0487154056279575"
}
```

Your mileage will vary.