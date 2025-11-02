import { query } from "../db/request/query";
import { ValidationError } from "../errors/validation-errors";
import {
  CreateScheduledTime,
  ScheduledTime,
} from "../models/scheduled-time.model";

export const createSheduleTimeRepo = async (
  data: CreateScheduledTime,
  taskId: string,
): Promise<ScheduledTime> => {
  const sqlRequest = `
    INSERT INTO scheduled_time (day, time_slots, task_id)
    VALUES ($1, $2, $3)
    RETURNING *;
  `;
  const res = await query<ScheduledTime>(sqlRequest, [
    data.day,
    data.timeSlots,
    taskId,
  ]);
  if (!res[0]) {
    throw new ValidationError("Failed to create scheduled time");
  }
  return res[0];
};
export const createSheduleTimesRepo = async (
  scheduledTime: CreateScheduledTime[],
  taskId: string,
): Promise<ScheduledTime[]> => {
  const newScheduledTimes: ScheduledTime[] = [];
  for (const elem of scheduledTime) {
    const newScheduledTime = await createSheduleTimeRepo(elem, taskId);
    newScheduledTimes.push(newScheduledTime);
  }
  return newScheduledTimes;
};
