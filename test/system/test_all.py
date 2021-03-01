import test.system.test_delete as delete
import test.system.test_get as get
import test.system.test_head as head
import test.system.test_post as post


if __name__ == "__main__":
    post.test()
    head.test()
    get.test()
    delete.test()
