import math
import concurrent.futures

# 计算调和级数的和
def calculate_harmonic_sum(n):
    if n <= 0:
        return 0.0

    # 对于极大值，只计算近似值
    if n > 1000000000:
        euler_mascheroni = 0.57721566490153286060651209008240243104215933593992
        return math.log(n) + euler_mascheroni + 1.0 / (2.0 * n)

    # 对于小值直接计算
    if n < 1000:
        sum = 0.0
        for i in range(1, n + 1):
            sum += 1.0 / i
        return sum

    # 对于大数值使用并发计算
    num_workers = 4
    chunk_size = n // num_workers
    total_sum = 0.0

    def calculate_chunk(start, end):
        local_sum = 0.0
        for j in range(start, end + 1):
            local_sum += 1.0 / j
        return local_sum

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # 提交任务
        futures = []
        for i in range(num_workers):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size
            futures.append(executor.submit(calculate_chunk, start, end))

        # 处理剩余部分
        remainder = n % num_workers
        if remainder > 0:
            start = num_workers * chunk_size + 1
            end = n
            futures.append(executor.submit(calculate_chunk, start, end))

        # 收集结果
        for future in concurrent.futures.as_completed(futures):
            total_sum += future.result()

    return total_sum

# 寻找调和级数和超过目标值的最小n
def find_n_for_target(target):
    if target <= 0:
        return 0

    # 防止整数溢出：当target > 44时，n会超过2^63-1
    if target > 44:
        return find_n_for_target_approximate(target, 1)

    euler_mascheroni = 0.57721566490153286060651209008240243104215933593992

    # 使用数学近似公式估算初始值
    # H_n ≈ ln(n) + γ + 1/(2n) - 1/(12n²) + 1/(120n⁴)
    # 反向求解：n ≈ e^(target - γ)

    # 防止指数溢出
    if target - euler_mascheroni > 700:
        # 如果指数太大，直接使用近似公式
        return find_n_for_target_approximate(target, 1)
    else:
        estimated_n = int(math.exp(target - euler_mascheroni))

    if estimated_n < 1:
        estimated_n = 1

    # 对于小目标值，直接使用精确计算
    if target <= 44:
        return find_n_for_target_exact(target, estimated_n)

    # 对于大目标值，使用近似公式
    return find_n_for_target_approximate(target, estimated_n)

def find_n_for_target_exact(target, start_n):
    n = start_n
    sum = calculate_harmonic_sum(n)

    # 检查是否已经溢出
    if math.isinf(sum) or math.isnan(sum):
        # 如果已经溢出，切换到近似方法
        return find_n_for_target_approximate(target, n)

    # 如果初始值已经超过目标，需要减小n
    if sum > target:
        while sum > target and n > 1:
            n -= 1
            sum = calculate_harmonic_sum(n)
            # 检查是否溢出
            if math.isinf(sum) or math.isnan(sum):
                return find_n_for_target_approximate(target, n)
        return n + 1

    # 否则增加n直到达到目标
    max_iterations = 10000000
    for _ in range(max_iterations):
        if sum >= target:
            break
        n += 1
        sum += 1.0 / n  # 增量计算，避免重新计算整个级数

        # 检查是否溢出
        if math.isinf(sum) or math.isnan(sum):
            return find_n_for_target_approximate(target, n)

    return n

def find_n_for_target_approximate(target, start_n):
    euler_mascheroni = 0.57721566490153286060651209008240243104215933593992

    # 使用牛顿迭代法求解
    # 我们需要找到n使得 H_(n) >= target且H_(n-1) < target
    # 使用近似公式 H_n ≈ ln(n) + γ + 1/(2n)

    n = float(start_n)
    if n < 1:
        n = 1.0

    for _ in range(100):
        # 防止n过小导致除零错误
        if n < 1e-10:
            n = 1.0

        # 计算当前近似值
        hn = math.log(n) + euler_mascheroni + 1.0 / (2.0 * n)

        # 检查是否溢出或无效
        if math.isinf(hn) or math.isnan(hn):
            # 如果计算出错，返回当前估计值
            result = int(n)
            if result < 1:
                result = 1
            return result

        # 计算误差
        error = hn - target

        # 如果误差足够小，返回结果
        if abs(error) < 1e-10:
            result = int(n)
            if result < 1:
                result = 1
            return result

        # 计算导数 dH_n/dn ≈ 1/n - 1/(2n²)
        derivative = 1.0 / n - 1.0 / (2.0 * n * n)

        # 防止导数过小导致数值不稳定
        if abs(derivative) < 1e-15:
            # 如果导数太小，直接返回当前值
            result = int(n)
            if result < 1:
                result = 1
            return result

        # 牛顿迭代：n_new = n - error/derivative
        delta = error / derivative

        # 限制步长，防止数值不稳定
        if abs(delta) > n * 0.5:
            delta = math.copysign(n * 0.5, delta)

        n = n - delta

        # 确保n为正数
        if n < 1:
            n = 1

        # 防止n过大
        if n > 1e20:
            result = int(n)
            if result < 1:
                result = 1
            return result

    result = int(n)
    if result < 1:
        result = 1

    return result

# 计算洛伦兹变换
def calculate_lorentz_transformation(x, t, v):
    light_speed = 299792458.0
    if v >= light_speed:
        raise ValueError("Velocity must be less than speed of light")

    gamma = 1.0 / math.sqrt(1.0 - (v * v) / (light_speed * light_speed))
    x_prime = gamma * (x - v * t)
    t_prime = gamma * (t - (v * x) / (light_speed * light_speed))

    return x_prime, t_prime, gamma

# 计算1~n的和
def calculate_sum_of_n(n):
    try:
        # 检查是否可能溢出
        if n > 10**18:
            raise OverflowError("Value too large")
        result = n * (n + 1) // 2
        # 检查结果是否溢出
        if result < 0:
            raise OverflowError("Result overflowed")
        return result
    except OverflowError:
        return None
