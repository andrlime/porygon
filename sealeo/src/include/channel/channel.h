#include <types.h>

#include <memory>
#include <semaphore>

namespace sealeo {
namespace channel {

template <typename T>
class Channel {
    using value_t = T;

private:
    value_t value; // TODO: use std::queue with capacity
    std::binary_semaphore sem_sender_ready{0}, sem_receiver_ready{0};
    bool closed = false;

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
    // Returns true if channel is closed, false if open
    inline bool
    is_closed()
    {
        return closed;
    }

    // Opens the channel. If already open, does nothing.
    inline void
    open()
    {
        closed = false;
    }

    // Closes the channel. If already closed, does nothing.
    inline void
    close()
    {
        closed = true;
    }

    // Reads a value from the channel. If there is no value, blocks until there is one.
    value_t
    recv()
    {
        sem_sender_ready.release();
        sem_receiver_ready.acquire();
        return get_value();
    }

    // Writes a value to the channel. Blocks until success.
    void
    send(const value_t& val)
    {
        sem_sender_ready.acquire();
        set_value(val);
        sem_receiver_ready.release();
    }

    // Overload << operator for channel << value
    inline void
    operator<<(const value_t& val)
    {
        send(val);
    }

    // Overload << operator for channel >> value
    inline void
    operator>>(value_t& val)
    {
        val = recv();
    }
};

} // namespace channel
} // namespace sealeo
