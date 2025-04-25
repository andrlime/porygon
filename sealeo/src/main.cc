#include <common.h>
#include <something/test.h>

#include <iostream>
#include <vector>

int
main()
{
    std::vector<NumberType> vec{1, 2, 3};
    std::cout << "Sum: " << foo(vec) << std::endl;
    return 0;
}
