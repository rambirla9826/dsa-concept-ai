# 20 High-Quality Seed Questions with Comprehensive Concept Blueprints for DSA

SEED_QUESTIONS = [
    # --- ARRAYS (3) ---
    {
        "id": "q_array_1",
        "title": "Two Sum",
        "category": "Arrays",
        "difficulty": "Easy",
        "problem_statement": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."}
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9"],
        "hints": [
            "Think about what complement number you need for each element.",
            "Can you trade space for time using a Hash Table to store previously seen numbers?",
            "Store number as key and index as value during a single pass."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "expected_edge_cases": ["Negative numbers in array", "Duplicate numbers that sum to target", "Target is zero"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Target Complement Calculation",
                "description": "Student calculates complement = target - current_element for each element.",
                "importance": "high",
                "weight": 20,
                "is_mandatory": True,
                "expected_keywords": ["complement", "target minus", "difference"]
            },
            {
                "concept_id": "C2",
                "concept_name": "HashMap/HashSet Data Structure Usage",
                "description": "Student uses a hash table to store visited numbers and their indices for O(1) lookup.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["hashmap", "hash table", "dictionary", "map"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Single Pass Traversal",
                "description": "Student explains checking if complement exists in hashmap before inserting current element.",
                "importance": "medium",
                "weight": 20,
                "is_mandatory": True,
                "expected_keywords": ["single pass", "one loop", "lookup", "check first"]
            },
            {
                "concept_id": "C4",
                "concept_name": "Index Returning",
                "description": "Student correctly identifies returning stored index and current loop index.",
                "importance": "low",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["index", "indices", "key value pair"]
            },
            {
                "concept_id": "C5",
                "concept_name": "Complexity Justification",
                "description": "Student explains O(n) time due to hash lookup and O(n) extra space for the map.",
                "importance": "high",
                "weight": 15,
                "is_mandatory": True,
                "expected_keywords": ["O(n)", "linear time", "space O(n)"]
            }
        ]
    },
    {
        "id": "q_array_2",
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "category": "Arrays",
        "difficulty": "Medium",
        "problem_statement": "Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The contiguous subarray [4,-1,2,1] has the largest sum = 6."}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "If the running sum becomes negative, does it help future subarrays?",
            "Decide whether to add current element to existing sum or start fresh from current element.",
            "Maintain a global maximum sum variable."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["All negative numbers", "Single element array", "All positive numbers"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Local vs Global Max State",
                "description": "Student maintains current_sum (local max) and max_so_far (global max).",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["current sum", "max sum", "global max", "running sum"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Reset Negative Sum Condition",
                "description": "Student recognizes if current running sum drops below 0 or current element, reset/start fresh.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["reset to 0", "start fresh", "max(num, current+num)", "drop negative"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Single Pass Dynamic Programming / Greedy",
                "description": "Student explains iterating through the array once in linear time.",
                "importance": "medium",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["one pass", "single loop", "kadane", "greedy"]
            },
            {
                "concept_id": "C4",
                "concept_name": "All-Negative Handling",
                "description": "Student accounts for cases where all elements are negative (max element returned).",
                "importance": "medium",
                "weight": 20,
                "is_mandatory": False,
                "expected_keywords": ["all negative", "largest negative", "initial max"]
            }
        ]
    },
    {
        "id": "q_array_3",
        "title": "Container With Most Water",
        "category": "Arrays",
        "difficulty": "Medium",
        "problem_statement": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "The vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. Maximum area is 49."}
        ],
        "constraints": ["n == height.length", "2 <= n <= 10^5", "0 <= height[i] <= 10^4"],
        "hints": [
            "Consider starting with the widest container using two pointers.",
            "Area is bottlenecked by the shorter wall.",
            "Move the pointer pointing to the shorter line inwards."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Two elements array", "Increasing height array", "Equal height lines"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Two Pointers Strategy",
                "description": "Student places left pointer at index 0 and right pointer at index n-1.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["two pointers", "left right pointer", "both ends"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Area Calculation Bottleneck",
                "description": "Student recognizes area = width * min(height[left], height[right]).",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["minimum height", "width times height", "bottleneck", "shorter line"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Greedy Pointer Shifting",
                "description": "Student moves the pointer at the shorter line inward to search for potentially taller lines.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["move shorter", "increment left", "decrement right", "taller height"]
            },
            {
                "concept_id": "C4",
                "concept_name": "Complexity Justification",
                "description": "Student proves O(n) time because pointers meet in center, and O(1) space.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["O(n)", "O(1) space", "constant space"]
            }
        ]
    },

    # --- STRINGS (2) ---
    {
        "id": "q_string_1",
        "title": "Valid Anagram",
        "category": "Strings",
        "difficulty": "Easy",
        "problem_statement": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.",
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true"},
            {"input": "s = \"rat\", t = \"car\"", "output": "false"}
        ],
        "constraints": ["1 <= s.length, t.length <= 5 * 10^4", "s and t consist of lowercase English letters."],
        "hints": [
            "Check length equality first.",
            "Count frequency of each character in s and decrement for t.",
            "Can use fixed array size 26 or HashMap."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Strings of different length", "Empty strings", "Unicode characters"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Length Pre-check",
                "description": "Student immediately checks if string lengths match; return false if unequal.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["length check", "different length", "lengths equal"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Character Frequency Counting",
                "description": "Student uses a hash table or fixed 26-element array to count letter frequencies.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["frequency count", "hashmap", "array 26", "character count"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Increment and Decrement Logic",
                "description": "Student increments counts for string s and decrements counts for string t.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["increment decrement", "subtract count", "all zero"]
            },
            {
                "concept_id": "C4",
                "concept_name": "Complexity Analysis",
                "description": "Student notes O(n) time and O(1) space because alphabet size is fixed to 26.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["O(n) time", "O(1) space", "constant 26"]
            }
        ]
    },
    {
        "id": "q_string_2",
        "title": "Longest Substring Without Repeating Characters",
        "category": "Strings",
        "difficulty": "Medium",
        "problem_statement": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "examples": [
            {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "The answer is \"abc\", with the length of 3."}
        ],
        "constraints": ["0 <= s.length <= 5 * 10^4"],
        "hints": [
            "Use a sliding window with left and right pointers.",
            "Use a Set or HashMap to keep track of characters in the current window.",
            "When a duplicate is encountered, shrink window from left."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(min(m, n))",
        "expected_edge_cases": ["Empty string", "All identical characters", "Single character string"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Sliding Window Pattern",
                "description": "Student uses left and right pointers defining a dynamic dynamic substring window.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["sliding window", "two pointers", "left right pointer"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Visited Character Tracking",
                "description": "Student uses a Set or HashMap to store current window characters and their latest indices.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["hashset", "set", "map index", "track characters"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Window Shrinking / Jump Logic",
                "description": "Student moves left pointer past the duplicate character position when a repeat is found.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["duplicate found", "shrink left", "jump left", "remove from set"]
            },
            {
                "concept_id": "C4",
                "concept_name": "Global Max Length Update",
                "description": "Student updates max_len = max(max_len, right - left + 1) at each step.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["max length", "window size", "update length"]
            }
        ]
    },

    # --- HASHING (2) ---
    {
        "id": "q_hash_1",
        "title": "Group Anagrams",
        "category": "Hashing",
        "difficulty": "Medium",
        "problem_statement": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        "examples": [
            {"input": "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "output": "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]" }
        ],
        "constraints": ["1 <= strs.length <= 10^4", "0 <= strs[i].length <= 100"],
        "hints": [
            "How can two anagrams produce the exact same key?",
            "You can sort each string to form a canonical key or use character frequency tuple.",
            "Map key -> list of anagram strings."
        ],
        "expected_time_complexity": "O(N * K log K)",
        "expected_space_complexity": "O(N * K)",
        "expected_edge_cases": ["Empty strings in list", "Single string array", "All distinct strings"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Canonical Hash Key Generation",
                "description": "Student recognizes that sorted string or 26-tuple frequency count serves as identical key for all anagrams.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["sorted string key", "frequency tuple", "canonical key", "hash key"]
            },
            {
                "concept_id": "C2",
                "concept_name": "HashMap Grouping Structure",
                "description": "Student uses HashMap<Key, List<String>> to group strings sharing the same key.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["hashmap list", "dictionary list", "map key to array"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Time Complexity Analysis",
                "description": "Student correctly identifies O(N * K log K) for sorting key or O(N * K) for character frequency key.",
                "importance": "medium",
                "weight": 25,
                "is_mandatory": False,
                "expected_keywords": ["O(N * K)", "sorting time", "k log k"]
            }
        ]
    },
    {
        "id": "q_hash_2",
        "title": "First Unique Character in a String",
        "category": "Hashing",
        "difficulty": "Easy",
        "problem_statement": "Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return `-1`.",
        "examples": [
            {"input": "s = \"leetcode\"", "output": "0"},
            {"input": "s = \"loveleetcode\"", "output": "2"}
        ],
        "constraints": ["1 <= s.length <= 10^5", "s consists of only lowercase English letters."],
        "hints": [
            "Use two passes over the string.",
            "Pass 1: Count frequency of each character into HashMap.",
            "Pass 2: Iterate string indices and check if character frequency is 1."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["No unique character exists", "First character is unique", "Single character string"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "First Pass Frequency Map",
                "description": "Student builds character frequency map in initial traversal.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["first pass", "count frequency", "hashmap"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Second Pass Index Order Verification",
                "description": "Student iterates through string sequentially checking for frequency == 1 to maintain original order.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["second pass", "check count 1", "preserve order", "return index"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Default Return -1 Handling",
                "description": "Student handles returning -1 if no unique character exists.",
                "importance": "low",
                "weight": 25,
                "is_mandatory": False,
                "expected_keywords": ["return -1", "no unique", "not found"]
            }
        ]
    },

    # --- BINARY SEARCH (2) ---
    {
        "id": "q_bs_1",
        "title": "Binary Search",
        "category": "Binary Search",
        "difficulty": "Easy",
        "problem_statement": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, return its index. Otherwise, return `-1`.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "nums is sorted in ascending order."],
        "hints": [
            "The array must be sorted.",
            "Compare target with middle element.",
            "Eliminate half of the search space at each iteration."
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Target smaller than min element", "Target larger than max element", "Single element array"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Sorted Array Prerequisite",
                "description": "Student specifies that the array must be sorted.",
                "importance": "high",
                "weight": 15,
                "is_mandatory": True,
                "expected_keywords": ["sorted array", "ascending order"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Boundary Initialization",
                "description": "Student initializes left = 0 and right = length - 1.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": True,
                "expected_keywords": ["left 0", "right n-1", "boundaries"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Middle Element Calculation",
                "description": "Student calculates mid = left + (right - left) // 2.",
                "importance": "high",
                "weight": 20,
                "is_mandatory": True,
                "expected_keywords": ["mid point", "middle element", "left + (right - left) / 2"]
            },
            {
                "concept_id": "C4",
                "concept_name": "Search Space Elimination",
                "description": "Student compares target with middle and eliminates half of array.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["eliminate half", "discard half", "cut search space"]
            },
            {
                "concept_id": "C5",
                "concept_name": "Boundary Updates",
                "description": "Student correctly sets left = mid + 1 or right = mid - 1.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": True,
                "expected_keywords": ["mid + 1", "mid - 1", "update pointers"]
            },
            {
                "concept_id": "C6",
                "concept_name": "O(log n) Complexity",
                "description": "Student states logarithmic time complexity.",
                "importance": "medium",
                "weight": 10,
                "is_mandatory": False,
                "expected_keywords": ["O(log n)", "logarithmic time"]
            }
        ]
    },
    {
        "id": "q_bs_2",
        "title": "Search in Rotated Sorted Array",
        "category": "Binary Search",
        "difficulty": "Medium",
        "problem_statement": "Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`. Algorithm time complexity must be O(log n).",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"}
        ],
        "constraints": ["1 <= nums.length <= 5000", "All values of nums are unique."],
        "hints": [
            "At least one half of the rotated array is always strictly sorted.",
            "Determine which half (left or right) is sorted.",
            "Check if target lies within the sorted half's boundaries."
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Array not rotated", "Target at pivot point", "Single element array"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "One Half Strictly Sorted Property",
                "description": "Student identifies that at least one half (left or right) is always sorted.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["one half sorted", "left half sorted", "right half sorted"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Sorted Half Detection",
                "description": "Student compares nums[left] <= nums[mid] to check if left half is sorted.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["compare nums[left] and nums[mid]", "identify sorted portion"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Target Range Search Decision",
                "description": "Student checks if target is within sorted bounds to decide which side to search.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["target between left and mid", "adjust pointers", "eliminate half"]
            }
        ]
    },

    # --- LINKED LIST (2) ---
    {
        "id": "q_ll_1",
        "title": "Reverse Linked List",
        "category": "Linked List",
        "difficulty": "Easy",
        "problem_statement": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"}
        ],
        "constraints": ["Number of nodes in list is in range [0, 5000]."],
        "hints": [
            "Use three pointers: prev, curr, next.",
            "Save curr.next before modifying pointer.",
            "Set curr.next = prev, then advance prev and curr."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Empty list (head == null)", "Single node list"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Three Pointers Tracking",
                "description": "Student initializes prev = null, curr = head, next_temp = null.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["prev", "curr", "next pointer", "three pointers"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Next Pointer Preservation",
                "description": "Student saves curr.next before overwriting link to prevent losing rest of list.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["save next", "temp next", "preserve link"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Pointer Reversal & Advancement",
                "description": "Student sets curr.next = prev, advances prev = curr and curr = temp_next.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["curr.next = prev", "advance prev", "move forward"]
            },
            {
                "concept_id": "C4",
                "concept_name": "New Head Return",
                "description": "Student returns prev as new head when curr reaches null.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["return prev", "prev is new head"]
            }
        ]
    },
    {
        "id": "q_ll_2",
        "title": "Detect Cycle in Linked List (Floyd's Cycle Finding)",
        "category": "Linked List",
        "difficulty": "Easy",
        "problem_statement": "Given `head`, the head of a linked list, determine if the linked list has a cycle in it.",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "true", "explanation": "There is a cycle in the linked list, where the tail connects to the 1st node."}
        ],
        "constraints": ["The number of the nodes in the list is in the range [0, 10^4]."],
        "hints": [
            "Can you solve it in O(1) memory?",
            "Use Fast and Slow pointers (Tortoise and Hare algorithm).",
            "Fast moves 2 steps, Slow moves 1 step."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Empty list", "Single node list with no cycle", "Two nodes with cycle"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Fast and Slow Pointers (Tortoise & Hare)",
                "description": "Student uses slow pointer moving 1 step and fast pointer moving 2 steps.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["slow pointer", "fast pointer", "tortoise and hare", "two steps one step"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Cycle Collision Condition",
                "description": "Student states that if slow == fast, a cycle exists.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["slow equals fast", "pointers meet", "collision"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Null Termination Check",
                "description": "Student recognizes that reaching fast == null or fast.next == null means no cycle.",
                "importance": "medium",
                "weight": 25,
                "is_mandatory": False,
                "expected_keywords": ["fast reaches null", "end of list", "no cycle"]
            }
        ]
    },

    # --- STACK/QUEUE (2) ---
    {
        "id": "q_sq_1",
        "title": "Valid Parentheses",
        "category": "Stack",
        "difficulty": "Easy",
        "problem_statement": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "examples": [
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false"}
        ],
        "constraints": ["1 <= s.length <= 10^4"],
        "hints": [
            "Last opened bracket must be first closed (LIFO).",
            "Push open brackets onto a Stack.",
            "When encountering a closed bracket, pop and verify matching type."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "expected_edge_cases": ["String starts with closing bracket", "Odd length string", "Unclosed opening brackets"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Stack LIFO Behavior",
                "description": "Student chooses Stack data structure for Last-In-First-Out matching.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["stack", "LIFO", "push pop"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Opening vs Closing Bracket Logic",
                "description": "Push open brackets; on close bracket pop stack and check matching pair.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["push opening", "pop matching", "bracket pair", "map closing to opening"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Empty Stack Final Validation",
                "description": "String is valid only if stack is completely empty at the end.",
                "importance": "medium",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["stack empty at end", "len == 0"]
            }
        ]
    },
    {
        "id": "q_sq_2",
        "title": "Implement Queue using Stacks",
        "category": "Queue",
        "difficulty": "Easy",
        "problem_statement": "Implement a first in first out (FIFO) queue using only two stacks.",
        "examples": [
            {"input": "push(1), push(2), peek(), pop(), empty()", "output": "returns 1, 1, false"}
        ],
        "constraints": ["1 <= x <= 9", "At most 100 calls total."],
        "hints": [
            "One stack for enqueue (push), one stack for dequeue (pop).",
            "Transfer elements from pushStack to popStack when popStack is empty."
        ],
        "expected_time_complexity": "O(1) amortized",
        "expected_space_complexity": "O(n)",
        "expected_edge_cases": ["Pop when popStack is empty", "Multiple consecutive pushes"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Two Stacks Architecture",
                "description": "Student uses instack (pushStack) and outstack (popStack).",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["two stacks", "instack outstack", "input output stack"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Lazy Element Transfer",
                "description": "When popping, if outstack is empty, pour all elements from instack into outstack.",
                "importance": "high",
                "weight": 45,
                "is_mandatory": True,
                "expected_keywords": ["transfer when empty", "pour elements", "reverse order"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Amortized O(1) Time Proof",
                "description": "Explains why pop operation is amortized O(1) because each element is moved at most twice.",
                "importance": "medium",
                "weight": 20,
                "is_mandatory": False,
                "expected_keywords": ["amortized O(1)", "constant amortized time"]
            }
        ]
    },

    # --- TREES (2) ---
    {
        "id": "q_tree_1",
        "title": "Maximum Depth of Binary Tree",
        "category": "Trees",
        "difficulty": "Easy",
        "problem_statement": "Given the `root` of a binary tree, return its maximum depth.",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3"}
        ],
        "constraints": ["The number of nodes in the tree is in range [0, 10^4]."],
        "hints": [
            "Think recursively.",
            "If root is null, depth is 0.",
            "Depth = 1 + max(depth(left), depth(right))."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(h)",
        "expected_edge_cases": ["Empty tree (root == null)", "Single node tree", "Skewed tree"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Base Case Identification",
                "description": "Student handles base case: if root is null return 0.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["base case null", "if root is null return 0"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Recursive Subproblem Breakdown",
                "description": "Student calculates left_depth = depth(root.left) and right_depth = depth(root.right).",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["recursion", "left child right child", "subtrees"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Max Combination Formula",
                "description": "Student returns 1 + max(left_depth, right_depth).",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["1 + max", "maximum of left and right"]
            }
        ]
    },
    {
        "id": "q_tree_2",
        "title": "Lowest Common Ancestor of a Binary Tree",
        "category": "Trees",
        "difficulty": "Medium",
        "problem_statement": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes `p` and `q`.",
        "examples": [
            {"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1", "output": "3"}
        ],
        "constraints": ["Number of nodes is in [2, 10^5].", "All Node.val are unique.", "p != q", "p and q exist in tree."],
        "hints": [
            "Recurse left and right subtrees.",
            "If current node is p or q, return current node.",
            "If both left and right calls return non-null, current node is the LCA."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(h)",
        "expected_edge_cases": ["One node is parent of the other", "Root is p or q"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Base Case Target Matching",
                "description": "If root is null or root == p or root == q, return root.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["root == p", "root == q", "return root"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Subtree Traversal Recursion",
                "description": "Recursively call search on left and right subtrees.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": True,
                "expected_keywords": ["left subtree", "right subtree", "recursive search"]
            },
            {
                "concept_id": "C3",
                "concept_name": "LCA Decision Rule",
                "description": "If both left and right return non-null, current node is LCA; else return non-null side.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["both non null", "current is LCA", "return non null child"]
            }
        ]
    },

    # --- GRAPHS (3) ---
    {
        "id": "q_graph_1",
        "title": "Number of Islands",
        "category": "Graphs",
        "difficulty": "Medium",
        "problem_statement": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.",
        "examples": [
            {"input": "grid = [[\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\"],[\"0\",\"0\",\"1\"]]", "output": "2"}
        ],
        "constraints": ["m == grid.length", "n == grid[i].length", "1 <= m, n <= 300"],
        "hints": [
            "Iterate through every cell in grid.",
            "When encountering '1', increment island count and trigger DFS/BFS.",
            "DFS/BFS marks all connected '1's as visited ('0')."
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "expected_edge_cases": ["All water grid", "All land grid", "1x1 grid"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Grid Traversal Loop",
                "description": "Student loops over all rows and columns of 2D matrix.",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": True,
                "expected_keywords": ["nested loop", "traverse grid", "each cell"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Island Detection & Counter",
                "description": "When cell == '1', increment island count and initiate traversal.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["when 1", "increment count", "trigger DFS"]
            },
            {
                "concept_id": "C3",
                "concept_name": "DFS/BFS Connected Component Traversal",
                "description": "Student uses DFS or BFS to visit all 4-directionally adjacent land cells.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["DFS", "BFS", "4 directions", "adjacent land"]
            },
            {
                "concept_id": "C4",
                "concept_name": "Visited Marking / Mutation",
                "description": "Student marks visited land cells (e.g. set to '0' or visited array) to avoid infinite loop.",
                "importance": "high",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["mark visited", "change to 0", "prevent revisit"]
            }
        ]
    },
    {
        "id": "q_graph_2",
        "title": "Detect Cycle in Undirected Graph",
        "category": "Graphs",
        "difficulty": "Medium",
        "problem_statement": "Given an undirected graph with `V` vertices and `E` edges, determine if the graph contains any cycle.",
        "examples": [
            {"input": "V = 5, E = 5, Edges = [[0,1],[1,2],[2,0],[1,3],[3,4]]", "output": "true", "explanation": "Cycle exists between 0 -> 1 -> 2 -> 0."}
        ],
        "constraints": ["1 <= V, E <= 10^5"],
        "hints": [
            "Use DFS or BFS with visited array and parent tracking.",
            "If an adjacent node is visited AND is not parent of current node, cycle detected!"
        ],
        "expected_time_complexity": "O(V + E)",
        "expected_space_complexity": "O(V)",
        "expected_edge_cases": ["Disconnected components", "Graph with no edges", "Self loops"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Visited Array & Parent Tracking",
                "description": "Student maintains a visited boolean array and passes parent node parameter in DFS/BFS.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["visited array", "parent node", "track parent"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Cycle Condition Detection",
                "description": "If neighbor is already visited AND neighbor != parent, a cycle is found.",
                "importance": "high",
                "weight": 45,
                "is_mandatory": True,
                "expected_keywords": ["visited and not parent", "neighbor != parent", "cycle detected"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Disconnected Components Traversal",
                "description": "Student loops over all V vertices to handle disconnected graphs.",
                "importance": "medium",
                "weight": 20,
                "is_mandatory": False,
                "expected_keywords": ["all vertices loop", "disconnected graph", "outer loop"]
            }
        ]
    },
    {
        "id": "q_graph_3",
        "title": "Shortest Path in Unweighted Graph (BFS)",
        "category": "Graphs",
        "difficulty": "Medium",
        "problem_statement": "Given an unweighted graph, find the shortest path (minimum number of edges) from a start node to a destination node.",
        "examples": [
            {"input": "Start = 0, End = 3, Edges = [[0,1],[0,2],[1,3],[2,3]]", "output": "2"}
        ],
        "constraints": ["1 <= V <= 10^4"],
        "hints": [
            "Why is BFS preferred over DFS for unweighted shortest path?",
            "BFS explores nodes level by level in order of distance.",
            "Maintain distance dictionary / queue."
        ],
        "expected_time_complexity": "O(V + E)",
        "expected_space_complexity": "O(V)",
        "expected_edge_cases": ["No path exists", "Start equals destination"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "BFS Selection Rationale",
                "description": "Student selects BFS because graph is unweighted and BFS visits level-by-level.",
                "importance": "high",
                "weight": 35,
                "is_mandatory": True,
                "expected_keywords": ["BFS", "breadth first search", "unweighted shortest path", "level by level"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Queue & Distance Tracking",
                "description": "Student uses Queue stores (node, distance) and a visited set.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["queue", "distance map", "visited set"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Early Exit / Unreachable Handling",
                "description": "Return distance immediately when destination is dequeued; return -1 if queue empties.",
                "importance": "medium",
                "weight": 25,
                "is_mandatory": False,
                "expected_keywords": ["return distance", "unreachable return -1"]
            }
        ]
    },

    # --- GREEDY (1) ---
    {
        "id": "q_greedy_1",
        "title": "Activity Selection / Non-overlapping Intervals",
        "category": "Greedy",
        "difficulty": "Medium",
        "problem_statement": "Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "examples": [
            {"input": "intervals = [[1,2],[2,3],[3,4],[1,3]]", "output": "1", "explanation": "[1,3] can be removed and the rest of intervals are non-overlapping."}
        ],
        "constraints": ["1 <= intervals.length <= 10^5"],
        "hints": [
            "Sort intervals by end time.",
            "Greedily select intervals that finish earliest.",
            "Count overlaps."
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["Already non-overlapping intervals", "All identical intervals"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Sort by End Time Strategy",
                "description": "Student explicitly sorts intervals by end time in ascending order.",
                "importance": "high",
                "weight": 45,
                "is_mandatory": True,
                "expected_keywords": ["sort by end time", "earliest finish time", "ascending end"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Greedy Overlap Comparison",
                "description": "Iterate intervals: if next_start < prev_end, increment removal count; else update prev_end.",
                "importance": "high",
                "weight": 40,
                "is_mandatory": True,
                "expected_keywords": ["start < end", "overlap", "increment count", "keep earliest end"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Complexity Proof",
                "description": "Sorting takes O(n log n) time and linear pass takes O(n).",
                "importance": "medium",
                "weight": 15,
                "is_mandatory": False,
                "expected_keywords": ["O(n log n)", "sorting complexity"]
            }
        ]
    },

    # --- DYNAMIC PROGRAMMING (1) ---
    {
        "id": "q_dp_1",
        "title": "Climbing Stairs",
        "category": "Dynamic Programming",
        "difficulty": "Easy",
        "problem_statement": "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, 2+1."}
        ],
        "constraints": ["1 <= n <= 45"],
        "hints": [
            "To reach step n, you can come from step (n-1) or step (n-2).",
            "dp[n] = dp[n-1] + dp[n-2].",
            "This matches the Fibonacci sequence."
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "expected_edge_cases": ["n = 1", "n = 2"],
        "concepts": [
            {
                "concept_id": "C1",
                "concept_name": "Subproblem Recurrence Relation",
                "description": "Student formulates ways(n) = ways(n-1) + ways(n-2).",
                "importance": "high",
                "weight": 45,
                "is_mandatory": True,
                "expected_keywords": ["dp[n-1] + dp[n-2]", "recurrence relation", "fibonacci"]
            },
            {
                "concept_id": "C2",
                "concept_name": "Base Cases Initialization",
                "description": "Student identifies base cases ways(1) = 1 and ways(2) = 2.",
                "importance": "medium",
                "weight": 25,
                "is_mandatory": True,
                "expected_keywords": ["base cases", "ways(1)=1", "ways(2)=2"]
            },
            {
                "concept_id": "C3",
                "concept_name": "Space Optimization (O(1) Space)",
                "description": "Student optimizes array to two variables (prev1, prev2) for O(1) space.",
                "importance": "high",
                "weight": 30,
                "is_mandatory": False,
                "expected_keywords": ["two variables", "constant space", "O(1) space"]
            }
        ]
    }
]
