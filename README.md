# Cab Pool Matcher

A command-line application for the end of semester rush. It keeps track of the cabs available,
collects ride requests from students, and puts students into cabs going to the same place at the same time. When seats are short, seniors get first pick.

Built for the SUTT Back-End Developer recruitment (Task 1).

## How to run

Python 3 is needed. No outside packages are used, only the standard library.

```
git clone https://github.com/plastichaircomb/cab-pool-matcher.git
cd cab-pool-matcher
python main.py
```

Run it from inside the project folder, due to the `cabs.json` file.

## Files

- `main.py` - the menu and all the core logic
- `models.py` - the `RideRequest` and `Cab` classes
- `cabs.json` - the list of cabs 

## Menu

| Option | What it does |
|---|---|
| 1 | Add a ride request (name, destination, time slot, year) |
| 2 | See waiting and all cabs |
| 3 | Find matches: preview |
| 4 | Send a specific cab |
| 5 | Dispatch by trip: pick a destination and slot|
| 0 | Quit |


## How it works

Every trip  has its own priority queue, stored in a dictionary. The queue belongs to the trip, not to any cab.

Each queue is a heap built with Python's `heapq`. Every entry is a tuple:

```
(-year, order, request)
```

- `heapq` always gives back the smallest item first, so the year is stored as a negative number.
  A 5th year becomes -5 and comes out before a 1st year (-1).
- `order` is a counter (1, 2, 3...) given to each request when it's added. If two students are in
  the same year, the one with the smaller order (who asked first) comes out first.

When a student adds a request, they just join their trip's queue. Nobody gets a seat until a cab
actually leaves. This is what lets a senior who signs up late still get ahead of a junior who signed up early.

- **Find Matches** looks at a sorted copy of the queue, so the real queue never changes.
- **Dispatch** pops students off the real queue, so they're removed from waiting and put in the cab.

Both use the same ordering, so the preview always shows exactly who the dispatch would take.

## Tricky situations

### 1. Half-empty cab
If the user tries to dispatch a cab with less than 50% of seats filled, it will be prompted with a confirmation, as a safety check. Option 4 allows the user to dispatch a cab, even if it  is empty. Once a cab has left, it is marked as left and no one can be added to it.

### 2. No cabs left
If every cab for a trip has left, new requests are still added to that trip's queue, and the student sees a message that there's no open cab right now. Students are only ever removed from a queue when a cab actually takes them, so they never disappear. Trying to dispatch that trip shows "No open cab".

### 3. Same year
Whenever a request is lodged, it is given a counter number, which helps the algorithm sort between same year ties by giving a higher priority to the request which was made first and has a lower counter number.

A counter number is used instead of using the timestamp of the request, because two requests can get the exact same timestamp (on Windows the clock updates every few milliseconds). Since every order number is unique, this method is foolproof.

### 4. Lots of students (say 1,000 waiting)
Here n is the number of students in a trip's queue and c is the number of cabs.

| Operation | Time | Why |

| Add one request | O(log n) | `heappush` on that trip's heap. |
| Add all 1,000 | O(n log n) | 1,000 pushes, each O(log n) |
| Send off one cab | O(log n) | Up to 4 `heappop`s, each O(log n). |
| Find an open cab for a trip | O(c) | Goes through the cab list in file order until it finds an open one for that trip |

Find Matches sorts a copy of each trip's queue, which is O(n log n).