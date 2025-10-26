import { Day } from "../enums/day.enum";

export interface CreateScheduledTime {
  day: Day;
  timeSlots: string[];
}
export interface ScheduledTime {
  id: string;
}
