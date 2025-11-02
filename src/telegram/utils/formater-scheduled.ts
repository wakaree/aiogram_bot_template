import { Task } from "../../models/task.model";

export const formatTaskSchedule = (task: Task) => {
  return task.scheduledTime
    .map((t) => `• ${t.day}: ${t.timeSlots.join(", ")}`)
    .join("\n");
};
