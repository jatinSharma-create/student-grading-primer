# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation


# Edge Case Documentation

### Identified Edge Case
What happens to the `/stats` endpoint computation if the database contains zero students, or if all students in the system have their `mark` field set to `null` (since mark is optional)?

### Why it needs to be handled
If an array aggregation is performed directly on an empty list of marks, python's `sum() / len()` calculation will cause a `ZeroDivisionError`, crashing the server container with a `500 Internal Server Error`. Additionally, calling `min()` or `max()` on an empty collection raises a `ValueError`.

### How it was addressed
In `backend/app.py` under the `/stats` route, we safely isolate all numeric marks into a list comprehension. Before any calculations take place, we explicitly evaluate if `count == 0`. If true, the route gracefully bypasses mathematical aggregates and safely returns `0` values across all stat properties with a successful `200 OK` network wrapper.