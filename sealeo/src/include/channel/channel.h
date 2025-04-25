#include <types.h>

#include <condition_variable>
#include <iostream>
#include <mutex>

namespace sealeo {
namespace channel {

template <typename T>
class Channel {
private:
    std::condition_variable sender_cv, receiver_cv;
    bool sender_waiting = false;
    bool receiver_waiting = false;

    T value;
    std::mutex mtx; // used for shared access to value

public:
    // Reads a value from the channel. If there is no value, blocks until there is one.
    T recv() {
        std::unique_lock<std::mutex> lock(mtx);

        while (!sender_waiting) {
            receiver_waiting = true;
            receiver_cv.wait(lock);
        }

        T result = value;
        receiver_waiting = false;
        sender_cv.notify_one();
        return result;
    }

    // Writes a value to the channel. Blocks until success.
    void send(const T& val) {
        std::unique_lock<std::mutex> lock(mtx);

        while (!receiver_waiting) {
            sender_waiting = true;
            sender_cv.wait(lock);
        }

        value = val;
        sender_waiting = false;
        receiver_cv.notify_one();
    }
};

}
} // namespace sealeo
