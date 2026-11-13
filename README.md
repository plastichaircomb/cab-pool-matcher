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


Each trip (a destination and time slot) has its own waiting queue.

When a ride request is added, the student is placed in that specific trip's queue. No seat is assigned
yet. Seats are allocated at the moment the cab is dispatched, to ensure that a senior who
submits a request later can still be placed ahead of a junior who submitted earlier.

Students in a queue are ordered by seniority. Students in the same year are ordered by when they submitted their request.


Each queue is a heap built with Python's `heapq`, storing entries of the form `(-year, order, request)`.
The year is stored as a negative number because `heapq` returns the smallest item first, so a 5th year (-5) is returned before a 1st year (-1). `order` is a counter assigned to each request and is used to break ties between students of the same year.


## Tricky situations

### 1. Half-empty cab
If the user tries to dispatch a cab with less than 50% of seats filled, it will be prompted with a confirmation, ensuring a cab cant leave empty by accident. Option 4 allows the user to dispatch a cab, even if it  is empty. Once a cab has left, it is marked as left and no one can be added to it.

### 2. No cabs left
If every cab for a trip has left, new requests are still added to that trip's queue, and the student sees a message that there's no open cab right now. Students are only ever removed from a queue when a cab actually takes them, so they never disappear. Trying to dispatch that trip shows "No open cab".

### 3. Same year
Whenever a request is lodged, it is given a counter number, which helps the algorithm sort between same year ties by giving a higher priority to the request which was made first and has a lower counter number.

A counter number is used instead of using the timestamp of the request, because two requests can get the exact same timestamp (on Windows the clock updates every few milliseconds). Since every order number is unique, this method is foolproof.

### 4. Lots of students (say 1,000)
Here n is the number of students in a trip's queue and c is the number of cabs.

| Operation | Time | Why |
|---|---|---|
| Add one request | O(log n) | `heappush` on that trip's heap.|
| Add all 1,000 | O(n log n) | 1,000 pushes |
| Send off one cab | O(log n) | Up to 4 `heappop`s, each O(log n). 4 is a constant. |
| Find an open cab for a trip | O(c) | Goes through the cab list until it finds an open one |


