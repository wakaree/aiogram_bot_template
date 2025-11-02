import { CreateTask } from "../../models/task.model";

export interface BotSession {
  __language_code?: string;
  createTaskData: CreateTask;
}
