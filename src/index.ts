import { connectDB } from "./db/connect";
import { intiBot } from "./telegram/bot";

const start = async () => {
  await connectDB();
  intiBot();
};
start();
