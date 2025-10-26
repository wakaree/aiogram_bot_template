import { ScheduledTime } from "./scheduled-time.model";

export interface CreateTask {
  title: string;
  description?: string;
  disposable: boolean;
  scheduledTime: ScheduledTime[];
}
export interface Task extends CreateTask {
  id: string;
}
