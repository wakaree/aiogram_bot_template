import { query } from "../db/request/query";
import { ValidationError } from "../errors/validation-errors";
import { CreateUser, User } from "../models/user.model";

export const createUserRepo = async (data: CreateUser): Promise<User> => {
  try {
    const sqlRequest = `
      INSERT INTO users (telegram_id, username, first_name, last_name)
      VALUES ($1, $2, $3, $4)
      RETURNING *;
    `;
    const res = await query<User>(sqlRequest, [
      data.telegramId,
      data.username,
      data.firstName,
      data.lastName,
    ]);

    return res[0];
  } catch (e) {
    if (e instanceof ValidationError) {
      throw e;
    }
    throw new ValidationError("Failed to create user");
  }
};

export const findOneByIdRepo = async (
  telegramId: number,
): Promise<User | undefined> => {
  const sqlRequest = `
    SELECT 
      u.telegram_id,
      u.username,
      u.first_name,
      u.last_name,
      u.created_at,
      COALESCE(
        json_agg(
          json_build_object(
            'chat_id', uc.chat_id,
            'user_id', uc.user_id
          )
        ) FILTER (WHERE uc.chat_id IS NOT NULL),
        '[]'
      ) AS user_chats
    FROM users u
    LEFT JOIN user_chats uc ON u.telegram_id = uc.user_id
    WHERE u.telegram_id = $1
    GROUP BY u.telegram_id, u.username, u.first_name, u.last_name, u.created_at;
  `;
  const res: User[] = await query(sqlRequest, [telegramId]);
  return res[0];
};
