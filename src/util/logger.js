// Structured JSON-lines logger (one object per line on stdout).

const LEVELS = { debug: 10, info: 20, warn: 30, error: 40 };

/**
 * @param {{ level?: string, name?: string, stream?: NodeJS.WritableStream }} [opts]
 */
export function createLogger({ level = 'info', name, stream = process.stdout } = {}) {
  const min = LEVELS[level] ?? LEVELS.info;

  const write = (lvl, msg, fields) => {
    if (LEVELS[lvl] < min) return;
    const entry = { ts: new Date().toISOString(), level: lvl, msg };
    if (name) entry.module = name;
    if (fields) Object.assign(entry, fields);
    stream.write(JSON.stringify(entry) + '\n');
  };

  return {
    debug: (msg, fields) => write('debug', msg, fields),
    info: (msg, fields) => write('info', msg, fields),
    warn: (msg, fields) => write('warn', msg, fields),
    error: (msg, fields) => write('error', msg, fields),
    child: (childName) =>
      createLogger({ level, name: name ? `${name}.${childName}` : childName, stream }),
  };
}
