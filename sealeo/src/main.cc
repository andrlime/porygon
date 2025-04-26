#include <channel/channel.h>

#include <iostream>
#include <thread>
#include <vector>

using sealeo::channel::Channel;

template <typename T>
void
sender(std::vector<T> numbers, std::shared_ptr<Channel<T>> channel)
{
    for (T elem : numbers) {
        *channel << elem;
    }

    channel->close();
    return;
}

template <typename T>
void
receiver(std::shared_ptr<Channel<T>> channel, size_t count)
{
    T val;
    while (!channel->is_closed()) {
        *channel >> val;
        std::cout << val << "\n";
    }

    return;
}

int
main()
{
    auto c = std::make_shared<Channel<int>>();
    std::vector<int> values{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    std::thread thread1(sender<int>, values, c);
    std::thread thread2(receiver<int>, c, values.size());

    thread1.join();
    thread2.join();
    return 0;
}
