#include <globals.h>
#include <logger/string_format.h>

#include <ctime>

#include <format>
#include <iostream>

namespace sealeo {

enum class LoggerLevel { DEBUG = 0, INFO, WARN, ERROR, MESSAGE };

class logger {
private:
    // Map levels to colorized strings
    const std::unordered_map<LoggerLevel, std::string> level_color_map_ = {
        {LoggerLevel::DEBUG,   sealeo::format::colorize_string(u"§9§lDEBUG§r")  },
        {LoggerLevel::INFO,    sealeo::format::colorize_string(u"§b§lINFO§r")   },
        {LoggerLevel::WARN,    sealeo::format::colorize_string(u"§e§lWARN§r")   },
        {LoggerLevel::ERROR,   sealeo::format::colorize_string(u"§c§lERROR§r")  },
        {LoggerLevel::MESSAGE, sealeo::format::colorize_string(u"§f§lMESSAGE§r")},
    };

    // Format string uses Minecraft color code formatters
    // Supports
    //      %name%: program name
    //      %level%: logger level (special -- uses the above map)
    //      %time%: timestamp
    //      %message%: message
    std::string format_string_ = sealeo::format::colorize_string(
        u"[%name%/%level%] (§f%time%§rZ) §r%message%§r"
    );

    // Current level: anything less won't be printed
    LoggerLevel current_level_;

    // Abstract log function. Rejects messages below current_level_ and applies
    // formatting
    void log(LoggerLevel level, std::string msg);

public:
    // Constructor and make singleton class
    logger(LoggerLevel level) : current_level_(level) {}

    logger(LoggerLevel level, std::u16string raw_format_string) :
        current_level_(level),
        format_string_(sealeo::format::colorize_string(raw_format_string))
    {}

    static logger&
    instance(LoggerLevel level)
    {
        static logger logger_instance(LoggerLevel::MESSAGE);
        logger_instance.set_level(level);
        return logger_instance;
    }

    inline void
    set_format_string(std::u16string raw_format_string)
    {
        format_string_ = sealeo::format::colorize_string(raw_format_string);
    }

    // Set log level: anything lower will not be printed
    inline void
    set_level(LoggerLevel new_level)
    {
        current_level_ = new_level;
    }

    // Loggers
    inline void
    debug(const std::string& msg)
    {
        log(LoggerLevel::DEBUG, msg);
    }

    inline void
    info(const std::string& msg)
    {
        log(LoggerLevel::INFO, msg);
    }

    inline void
    warn(const std::string& msg)
    {
        log(LoggerLevel::WARN, msg);
    }

    inline void
    error(const std::string& msg)
    {
        log(LoggerLevel::ERROR, msg);
    }

    inline void
    msg(const std::string& msg)
    {
        log(LoggerLevel::MESSAGE, msg);
    }
};

} // namespace sealeo
