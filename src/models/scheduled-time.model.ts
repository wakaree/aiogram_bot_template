import { Day } from "../enums/day.enum";

export interface ScheduledTime {
  day: Day;
  timeSlots: string[];
}
