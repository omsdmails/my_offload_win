from offload_lib import offload
import time
import math
import numpy as np
from typing import Dict, List, Union

# ============= وظائف مساعدة =============
def _validate_positive_integer(value: int, name: str) -> None:
    """تحقق من أن القيمة عدد صحيح موجب."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} يجب أن يكون عددًا صحيحًا موجبًا")

# ============= المهام الرئيسية =============
@offload
def matrix_multiply(size: int) -> Dict[str, List[List[float]]]:
    """
    ضرب مصفوفات كبير (عملية كثيفة الحساب)
    
    Args:
        size: حجم المصفوفة (size x size)
    
    Returns:
        نتيجة الضرب كقائمة ثنائية الأبعاد
    """
    _validate_positive_integer(size, "حجم المصفوفة")
    
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return {"result": np.dot(A, B).tolist()}

@offload
def prime_calculation(n: int) -> Dict[str, Union[int, List[int]]]:
    """
    حساب الأعداد الأولية حتى n
    
    Args:
        n: الحد الأعلى للبحث عن الأعداد الأولية
    
    Returns:
        قامة بالأعداد الأولية وعددها
    """
    _validate_positive_integer(n, "الحد الأعلى للأعداد الأولية")
    
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return {"primes_count": len(primes), "primes": primes}

@offload
def data_processing(data_size: int) -> Dict[str, int]:
    """
    محاكاة معالجة بيانات كبيرة
    
    Args:
        data_size: عدد عناصر البيانات المراد معالجتها
    
    Returns:
        عدد العناصر المعالجة
    """
    _validate_positive_integer(data_size, "حجم البيانات")
    
    processed_data = []
    for i in range(data_size):
        result = sum(math.sin(x) * math.cos(x) for x in range(i, i+100))
        processed_data.append(result)
    return {"processed_items": len(processed_data)}

@offload
def image_processing_emulation(iterations: int) -> Dict[str, Union[int, float]]:
    """
    محاكاة معالجة الصور (عملية كثيفة الحساب)
    
    Args:
        iterations: عدد التكرارات للمحاكاة
    
    Returns:
        نتائج المحاكاة
    """
    _validate_positive_integer(iterations, "عدد التكرارات")
    
    results = []
    for i in range(iterations):
        value = sum(math.exp(math.sin(x)) for x in range(i, i+50))
        results.append(value)
    return {"iterations": iterations, "result": sum(results)}

# ============= اختبار الوظائف محلياً =============
if __name__ == "__main__":
    # اختبار جميع الوظائف مع معالجة الأخطاء
    test_cases = [
        ("matrix_multiply", matrix_multiply, 100),
        ("prime_calculation", prime_calculation, 1000),
        ("data_processing", data_processing, 500),
        ("image_processing", image_processing_emulation, 50)
    ]
    
    for name, func, arg in test_cases:
        try:
            print(f"\nجارِ تشغيل: {name}...")
            start = time.time()
            result = func(arg)
            duration = time.time() - start
            
            print(f"النتيجة: {str(result)[:200]}...")
            print(f"الوقت المستغرق: {duration:.2f} ثانية")
        except Exception as e:
            print(f"فشل {name}: {str(e)}")
