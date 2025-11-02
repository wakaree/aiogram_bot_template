import dotenv from "dotenv";
dotenv.config();

export const configVerify = (name: string): string => {
  const value = process.env[name];
  if (!value) {
    throw new Error(`❌ Environment variable "${name}" is missing`);
  }
  return value;
};
