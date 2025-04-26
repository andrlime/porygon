#include <logger/logger.h>

namespace sealeo {

void
logger::log(LoggerLevel level, std::string msg)
{
    if (level < current_level_)
        return;

    time_t timestamp;
    time(&timestamp);
    auto timestamp_string = std::to_string(timestamp);

    std::string output = format_string_;
    output = format::replace_string(output, "name", sealeo::globals::name);

    output = format::replace_string(output, "level", level_color_map_.at(level));
    output = format::replace_string(output, "lvl", level_color_map_.at(level));
    output = format::replace_string(output, "l", level_color_map_.at(level));

    output = format::replace_string(output, "timestamp", timestamp_string);
    output = format::replace_string(output, "time", timestamp_string);
    output = format::replace_string(output, "t", timestamp_string);

    output = format::replace_string(output, "message", msg);
    output = format::replace_string(output, "msg", msg);
    output = format::replace_string(output, "m", msg);

    std::cout << output << "\n";
}

} // namespace sealeo
