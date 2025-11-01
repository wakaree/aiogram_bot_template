import { CreateScheduledTime, ScheduledTime } from "./scheduled-time.model";

export interface TaskBase {
  title: string;
  description?: string;
  disposable: boolean;
}
export interface CreateTask extends TaskBase {
  scheduledTime: CreateScheduledTime[];
}
export interface Task extends TaskBase {
  id: string;
  scheduledTime: ScheduledTime[];
}
