# Meeting Scheduler - User Journey

## Main Booking Flow

### Step 1: Select Advisor
- **API:** `GET /advisors`
- **Action:** Display list of advisors for selection

### Step 2: View Availability
- **API:** `GET /advisors/{advisorId}/availability?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`
- **Action:** Display calendar with available time slots (30 min / 60 min)

### Step 3: Book Meeting
- **API:** `POST /meetings`
- **Action:** Create booking with selected slot, duration, and attendee details
- **Returns:** Meeting confirmation

---

## Additional Flows

### View My Meetings
- **API:** `GET /meetings?attendeeEmail=email@example.com`
- **Action:** List user's booked meetings

### View Meeting Details
- **API:** `GET /meetings/{meetingId}`
- **Action:** Show meeting information

### Reschedule Meeting
- **API:** `PATCH /meetings/{meetingId}`
- **Action:** Update meeting time/duration

### Cancel Meeting
- **API:** `DELETE /meetings/{meetingId}`
- **Action:** Cancel booking and free up slot

---

## API Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/advisors` | GET | List all advisors |
| `/advisors/{advisorId}` | GET | Get advisor details |
| `/advisors/{advisorId}/availability` | GET | Get available time slots |
| `/meetings` | POST | Book a meeting |
| `/meetings` | GET | List meetings (with filters) |
| `/meetings/{meetingId}` | GET | Get meeting details |
| `/meetings/{meetingId}` | PATCH | Update meeting |
| `/meetings/{meetingId}` | DELETE | Cancel meeting |
