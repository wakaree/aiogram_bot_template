"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.webhookCallback = webhookCallback;
const platform_node_js_1 = require("../platform.node.js");
const frameworks_js_1 = require("./frameworks.js");
const debugErr = (0, platform_node_js_1.debug)("grammy:error");
const callbackAdapter = (update, callback, header, unauthorized = () => callback('"unauthorized"')) => ({
    update: Promise.resolve(update),
    respond: callback,
    header,
    unauthorized,
});
const adapters = { ...frameworks_js_1.adapters, callback: callbackAdapter };
function webhookCallback(bot, adapter = platform_node_js_1.defaultAdapter, onTimeout, timeoutMilliseconds, secretToken) {
    if (bot.isRunning()) {
        throw new Error("Bot is already running via long polling, the webhook setup won't receive any updates!");
    }
    else {
        bot.start = () => {
            throw new Error("You already started the bot via webhooks, calling `bot.start()` starts the bot with long polling and this will prevent your webhook setup from receiving any updates!");
        };
    }
    const { onTimeout: timeout = "throw", timeoutMilliseconds: ms = 10000, secretToken: token, } = typeof onTimeout === "object"
        ? onTimeout
        : { onTimeout, timeoutMilliseconds, secretToken };
    let initialized = false;
    const server = typeof adapter === "string"
        ? adapters[adapter]
        : adapter;
    return async (...args) => {
        var _a;
        const handler = server(...args);
        if (!initialized) {
            // Will dedupe concurrently incoming calls from several updates
            await bot.init();
            initialized = true;
        }
        if (handler.header !== token) {
            await handler.unauthorized();
            return handler.handlerReturn;
        }
        let usedWebhookReply = false;
        const webhookReplyEnvelope = {
            async send(json) {
                usedWebhookReply = true;
                await handler.respond(json);
            },
        };
        await timeoutIfNecessary(bot.handleUpdate(await handler.update, webhookReplyEnvelope), typeof timeout === "function" ? () => timeout(...args) : timeout, ms);
        if (!usedWebhookReply)
            (_a = handler.end) === null || _a === void 0 ? void 0 : _a.call(handler);
        return handler.handlerReturn;
    };
}
function timeoutIfNecessary(task, onTimeout, timeout) {
    if (timeout === Infinity)
        return task;
    return new Promise((resolve, reject) => {
        const handle = setTimeout(() => {
            debugErr(`Request timed out after ${timeout} ms`);
            if (onTimeout === "throw") {
                reject(new Error(`Request timed out after ${timeout} ms`));
            }
            else {
                if (typeof onTimeout === "function")
                    onTimeout();
                resolve();
            }
            const now = Date.now();
            task.finally(() => {
                const diff = Date.now() - now;
                debugErr(`Request completed ${diff} ms after timeout!`);
            });
        }, timeout);
        task.then(resolve)
            .catch(reject)
            .finally(() => clearTimeout(handle));
    });
}
