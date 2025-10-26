import "dotenv/config";
import { configVerify } from "../utils/confif-verify";

export const botConfig = {
  bot_token: configVerify("BOT_TOKEN"),
};
