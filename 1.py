def subsets(nums):
    result = []
    path = []

    def backtrack(i):
        if i == len(nums):
            result.append(path.copy())
            return

        # 不选当前数字，直接处理下一个
        backtrack(i + 1)

        # 选当前数字
        # ① 加入 path
        # ② 递归处理下一个
        # ③ 撤销选择
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()

    backtrack(0)
    return result