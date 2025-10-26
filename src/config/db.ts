import { configVerify } from "../utils/confif-verify";

export const dbConfig = {
  user: configVerify("POSTGRES_USER"),
  host: configVerify("DB_HOST") || "localhost",
  database: configVerify("POSTGRES_DB"),
  password: configVerify("POSTGRES_PASSWORD"),
  port: Number(process.env.DB_PORT) || 5432,
};
