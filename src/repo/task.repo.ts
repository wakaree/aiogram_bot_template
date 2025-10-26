import { query } from "../db/request/query";
import { CreateTask, Task } from "../models/task.model";
import { createSheduleTime } from "./sheduled-time.repo";

export const createTask = async (data: CreateTask) => {
  try {
    const sqlRequest = `
    INSERT INTO tasks (title, disposable, description)
    VALUES ($1, $2, $3)
    RETURNING *;
  `;
    const res = await query<Task>(sqlRequest, [
      data.title,
      data.disposable,
      data.description,
    ]);
    for (const elem of data.scheduledTime) {
      await createSheduleTime(elem, res[0].id);
    }
    return res[0];
  } catch (e) { }
};
