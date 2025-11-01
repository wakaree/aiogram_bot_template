import { query } from "../db/request/query";
import { ValidationError } from "../errors/validation-errors";
import { CreateUserChat, UserChat } from "../models/user-chat.model";

export const createUserChatRepo = async (data: CreateUserChat) => {
  try {
    const sqlRequest = `
      INSERT INTO user_chats (chat_id, user_id)
      VALUES ($1, $2)
      RETURNING *;
    `;
    const res = await query<UserChat>(sqlRequest, [data.chatId, data.userId]);

    if (!res.length) {
      throw new ValidationError("User chat not created");
    }
    return res[0];
  } catch (e) {
    if (e instanceof ValidationError) {
      throw e;
    }
    throw new ValidationError("Failed to create user chat");
  }
};
