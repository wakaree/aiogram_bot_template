import { UserChat } from "./user-chat.model";

export interface CreateUser {
  telegramId: number;
  username?: string;
  firstName?: string;
  lastName?: string;
}
export interface User extends CreateUser {
  createdAt: Date;
  userChats: UserChat[];
}
