import "dotenv/config";
import { configVerify } from "../utils/config-verify";

export const botConfig = {
  bot_token: configVerify("BOT_TOKEN"),
};
