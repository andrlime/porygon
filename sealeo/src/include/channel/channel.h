#include <types.h>

#include <condition_variable>

#include <iostream>
#include <mutex>
#include <semaphore>

namespace sealeo {
namespace channel {

template <typename T>
class Channel {
    using value_t = T;

private:
    value_t value;
    std::binary_semaphore sem_sender_ready{0}, sem_receiver_ready{0};

    inline void
    set_value(const value_t& v)
    {
        value = v;
    }

    inline value_t
    get_value() const
    {
        return value;
    }

public:
    // Reads a value from the channel. If there is no value, blocks until there is one.
    value_t
    recv()
    {
        sem_sender_ready.release();
        auto result = get_value();
        sem_receiver_ready.acquire();
        return result;
    }

    // Writes a value to the channel. Blocks until success.
    void
    send(const value_t& val)
    {
        sem_sender_ready.acquire();
        set_value(val);
        sem_receiver_ready.release();
    }
};

} // namespace channel
} // namespace sealeo
