import { ValidationError } from "../errors/validation-errors";
import { CreateTask, Task } from "../models/task.model";
import { createFullTaskRepo } from "../repo/task.repo";

export const createTaskService = async (
  data: CreateTask,
  useChatId: number,
): Promise<Task> => {
  try {
    return createFullTaskRepo(data, useChatId);
  } catch (e) {
    if (e instanceof ValidationError) {
      throw e;
    }
    throw new ValidationError("Failed to create user");
  }
};
