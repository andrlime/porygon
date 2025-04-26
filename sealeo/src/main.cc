#include <channel/channel.h>

#include <thread>
#include <vector>

using sealeo::channel::Channel;

template <typename T>
void
sender(std::vector<T> numbers, std::shared_ptr<Channel<T>> channel)
{
    for (T elem : numbers) {
        std::cout << "Sent " << elem << std::endl;
        channel->send(elem);
    }

    return;
}

template <typename T>
void
receiver(std::shared_ptr<Channel<T>> channel, size_t count)
{
    while (true) {
        T val = channel->recv();
        std::cout << "Received " << val << std::endl;
    }

    return;
}

int
main()
{
#ifdef _LIBCPP_STD_VER
    std::cout << "_LIBCPP_STD_VER = " << _LIBCPP_STD_VER << "\n";
#else
    std::cout << "_LIBCPP_STD_VER is NOT defined\n";
#endif

    auto c = std::make_shared<Channel<int>>();
    std::vector<int> values{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    std::thread thread1(sender<int>, values, c);
    std::thread thread2(receiver<int>, c, values.size());

    // thread1.join();
    // thread2.join();
    while (true) {}

    return 0;
}
