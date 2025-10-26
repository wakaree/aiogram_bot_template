import { query } from "../db/request/query";
import { ScheduledTime } from "../models/scheduled-time.model";

export const createSheduleTime = async (
  data: ScheduledTime,
  taskId: string,
) => {
  const sqlRequest = `
    INSERT INTO tasks (day, timeSlots, task_id)
    VALUES ($1, $2, $3)
    RETURNING *;
  `;
  const res = await query(sqlRequest, [data.day, data.timeSlots, taskId]);
  return res[0];
};
