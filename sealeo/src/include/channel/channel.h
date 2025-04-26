#include <types.h>

#include <memory>
#include <semaphore>

namespace sealeo {

template <typename value_t>
class channel {
private:
    value_t value_; // TODO: use std::queue with capacity
    std::binary_semaphore sem_sender_ready_{0}, sem_receiver_ready_{0};
    bool closed_ = false;

    inline void
    set_value(const value_t& v)
    {
        value_ = v;
    }

    inline value_t
    get_value() const
    {
        return value_;
    }

public:
    // This channel's pointer type
    using pointer_t = std::shared_ptr<channel<value_t>>;

    // Static constructor that creates a shared pointer
    inline static pointer_t
    create_channel()
    {
        return std::make_shared<channel<value_t>>();
    }

    // Returns true if channel is closed, false if open
    inline bool
    is_closed()
    {
        return closed_;
    }

    // Opens the channel. If already open, does nothing.
    inline void
    open()
    {
        closed_ = false;
    }

    // Closes the channel. If already closed, does nothing.
    inline void
    close()
    {
        closed_ = true;
    }

    // Reads a value from the channel. If there is no value, blocks until there is one.
    value_t
    recv()
    {
        sem_sender_ready_.release();
        sem_receiver_ready_.acquire();
        return get_value();
    }

    // Writes a value to the channel. Blocks until success.
    void
    send(const value_t& val)
    {
        sem_sender_ready_.acquire();
        set_value(val);
        sem_receiver_ready_.release();
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

} // namespace sealeo
