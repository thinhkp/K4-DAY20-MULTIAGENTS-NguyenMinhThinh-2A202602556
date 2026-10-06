Hiểu bài toán và lấy repo
Phần 0: Cài đặt & Làm quen
Khoảng 45 phút. Bạn fork repo, tạo môi trường, cài thư viện, và làm quen với multi-agent framework.

Sau phần này, toàn bộ môi trường sẵn sàng để implement. Không tốn token.

0.1. Cài đặt
Hành động
Fork repo (nếu chưa có):

Truy cập VinUni-AI20k/K4-L3L4-Track3-Day20-AdvanceMultiAgents
Bấm Fork → đặt tên K4-DAY20-MULTIAGENTS-<HoVaTen>-<MSSV>
Clone về máy:

git clone https://github.com/<your-username>/K4-DAY20-MULTIAGENTS-HoVaTen-MSSV.git
cd K4-DAY20-MULTIAGENTS-HoVaTen-MSSV
code .
Chép
Tạo Virtual Environment:

Windows: py -3.11 -m venv .venv + .venv\Scripts\activate
macOS/Linux: python3.11 -m venv .venv + source .venv/bin/activate
Cài đặt thư viện:

pip install -r requirements.txt
Chép
Tạo .env từ mẫu:

cp .env.example .env  # hoặc: copy .env.example .env (Windows)
Chép
Mở .env và điền: OPENAI_API_KEY=sk-...

Tạo báo cáo từ mẫu:

cp report/REPORT.template.md report/REPORT.md
Chép
Bật UTF-8 trên Windows (nếu dùng PowerShell):

$env:PYTHONIOENCODING="utf-8"
Chép
0.2. Kiểm tra môi trường
Test 1: Kiểm tra 6 tác vụ
pytest tests/test_01_provided.py -q
Chép
✅ Kỳ vọng:

12 passed
Chép
Nếu fail: kiểm tra đã activate venv? Đã cài -e .?

Test 2: Kiểm tra kết nối mô hình
python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').content)"
Chép
✅ Kỳ vọng:

OK
Chép
Nếu lỗi AuthenticationError: kiểm tra OPENAI_API_KEY trong .env.

0.3. Khám phá Cấu trúc Repo
ls -la
cat README.md
cat LAB_GUIDE.md  # (nếu có)
Chép
⚠️ Không tốn token (chỉ đọc tài liệu).

Script/tài liệu sẽ cung cấp:

Tổng quan về multi-agent architecture
Danh sách các agent cần implement
Mô tả của mỗi component (coordinator, worker agents, tools)
System prompt và configuration mẫu
Trả lời 3 câu vào report/REPORT.md mục 3
Câu 1: Bài lab này có bao nhiêu agent? Mỗi agent làm gì?

Ví dụ trả lời:

Có 3-4 agent chính:
- Coordinator: điều phối và gán task cho worker agents
- Worker Agent 1: xử lý loại task A (ví dụ: data analysis)
- Worker Agent 2: xử lý loại task B (ví dụ: code generation)
- [Optional] Evaluator: đánh giá chất lượng output

Mỗi agent có công cụ riêng (tools) phù hợp với chuyên môn.
Chép
Câu 2: Coordinator giao tiếp với worker agents bằng cách nào?

Ví dụ trả lời:

Coordinator gửi task description đến worker agents qua:
- Message queue / API calls
- Agent chọn công cụ phù hợp để xử lý
- Return kết quả về coordinator
- Coordinator có thể verify hoặc gán task tiếp theo.
Chép
Câu 3: Có những công cụ (tools) nào được chia sẻ giữa các agent?

Ví dụ trả lời:

Các công cụ chia sẻ:
- Logging & monitoring: tất cả agent đều ghi log
- Knowledge base retrieval: tìm kiếm thông tin chung
- Common utilities: validation, data transformation
Chép
⚠️ Lưu ý quan trọng
.env đã trong .gitignore → Không bao giờ commit .env hoặc dán key vào code!
Commit key sẽ bị trừ 20 điểm
Kiểm tra: cat .gitignore | grep .env
Multi-agent communication có thể phức tạp → hãy debug từng agent riêng biệt trước
Checklist Phần 0
 Fork repo thành công
 Clone về + mở VS Code
 Activate venv
 Cài pip install -e . (hoặc pip install -r requirements.txt)
 Tạo .env + điền key OpenAI
 Test kết nối mô hình thành công
 Tạo report/REPORT.md (từ template nếu có)
 Đọc README.md + LAB_GUIDE.md
 Trả lời 3 câu vào báo cáo mục 3
 Kiểm tra các file config (agent definitions, tool configurations)


 Kiến trúc tổng thể
Thuật ngữ gốc	Bản chất khái niệm	Minh hoạ trực quan
Agent	Một "nhân viên" LLM có vai trò, prompt và công cụ riêng, nhận input từ state và trả output có cấu trúc	Researcher như thực tập sinh chuyên đi tìm tài liệu; Writer như biên tập viên chỉ lo viết
Supervisor / Router	Agent điều phối: nhìn state hiện tại và quyết định bước tiếp theo là gọi ai hoặc dừng	Trưởng nhóm đứng bảng phân công: "chưa có nguồn → gọi Researcher; đủ phân tích → gọi Writer"
Shared state	Cấu trúc dữ liệu duy nhất được truyền qua mọi agent, chứa toàn bộ ngữ cảnh của phiên làm việc	Tờ hồ sơ vụ việc chuyền tay trong văn phòng — ai làm xong phần mình thì ghi thêm vào
Handoff	Việc một agent hoàn thành và chuyển quyền xử lý (kèm state) cho agent khác	Researcher nộp research_notes vào hồ sơ rồi chuyển bàn cho Analyst
LangGraph	Framework xây workflow dạng đồ thị: node là agent, edge là luồng chuyển, có conditional routing	Sơ đồ dây chuyền sản xuất: mỗi trạm một việc, có nhánh rẽ tùy tình trạng sản phẩm
Guardrail	Cơ chế chặn agent chạy sai/vô hạn: max iterations, timeout, retry, validation	Cầu dao tự ngắt — vòng lặp Supervisor↔Researcher quá 6 lần thì hệ thống dừng, không đốt token vô ích
Trace	Bản ghi từng bước chạy: agent nào được gọi, input/output gì, tốn bao nhiêu token/thời gian	Hộp đen máy bay — khi kết quả sai, mở trace ra xem sai từ bước nào
Benchmark	So sánh có số liệu giữa các cách làm (latency, cost, quality) thay vì cảm tính	Đua hai đội cùng đề bài, chấm bằng đồng hồ + hóa đơn token + rubric, không chấm bằng "trông có vẻ hay"


Implement Coordinator Agent
Phần 2: Implement Coordinator Agent
Khoảng 4-5 giờ. Bạn cài đặt coordinator - agent trung tâm nhận user request, phân tích, định tuyến đến worker agents, và aggregating kết quả.

Không tốn token. Mục đích: xây dựng "trái tim" của system.

2.1. Hiểu Coordinator Responsibilities
Hành động
Đọc tài liệu coordinator (nếu có):

cat src/coordinator.py  # Xem TODO + docstring
cat src/base_agent.py   # Xem base class
Chép
Coordinator phải làm gì:
Receive request từ user (string text hoặc structured)
Analyze task - loại task gì? Cần agent nào?
Route to workers - gửi task description đến phù hợp worker
Wait for results - coordinator chờ (với timeout)
Aggregate/Verify - kết hợp kết quả từ multiple workers
Return response - trả về user
Ví dụ flow:
User: "Tính tổng doanh thu Q3 và tạo biểu đồ"
  ↓
Coordinator analyze: cần 2 workers
  ├→ Task 1: Data Agent (tính tổng)
  └→ Task 2: Code Agent (tạo biểu đồ)
  ↓
Wait for both (timeout=60s)
  ├← Data Agent: "Tổng: 5M USD"
  └← Code Agent: "Biểu đồ: <image_path>"
  ↓
Aggregate: "Tổng doanh thu Q3: 5M USD. [Biểu đồ đính kèm]"
  ↓
Return to User
Chép
2.2. Cài đặt Coordinator
Hành động
Mở file:

code src/coordinator.py
Chép
Tìm hàm TODO (thường 3-5 hàm):

def __init__(self):
    # TODO: Initialize coordinator state
    pass

def parse_request(self, user_input):
    # TODO: Extract task type, parameters
    pass

def route_task(self, task_type, content):
    # TODO: Determine which worker agent(s) to call
    pass

def execute_tasks(self, tasks):
    # TODO: Send tasks, wait for results, handle timeout
    pass

def aggregate_results(self, results):
    # TODO: Combine results, format response
    pass
Chép
Cài đặt từng hàm
__init__:

def __init__(self, model, worker_agents, message_queue=None):
    self.model = model
    self.workers = {agent.name: agent for agent in worker_agents}
    self.task_queue = message_queue or MessageQueue()
    self.active_tasks = {}  # Track ongoing tasks
    self.logger = get_logger("coordinator")
Chép
parse_request:

def parse_request(self, user_input):
    """Extract task type and parameters from user input"""
    prompt = f"""
    Analyze this user request and determine:
    1. Task type (data_analysis, code_generation, evaluation, etc.)
    2. Required parameters
    3. Priority
    
    User request: {user_input}
    """
    response = self.model.invoke(prompt)
    # Parse response into structured format
    return {
        "task_type": extracted_type,
        "parameters": extracted_params,
        "priority": extracted_priority
    }
Chép
route_task:

def route_task(self, task_type, content):
    """Route task to appropriate worker(s)"""
    routing_map = {
        "data_analysis": ["data_agent"],
        "code_generation": ["code_agent"],
        "evaluation": ["evaluator_agent"],
        "complex": ["data_agent", "code_agent"]  # Multiple workers
    }
    return routing_map.get(task_type, ["data_agent"])
Chép
execute_tasks:

def execute_tasks(self, tasks, timeout=60):
    """Execute tasks on worker agents, wait for results"""
    results = {}
    futures = {}
    
    for task in tasks:
        # Send task to worker
        worker = self.workers[task['worker']]
        future = worker.process_async(task['content'])
        futures[task['id']] = future
    
    # Wait for all with timeout
    import asyncio
    try:
        results = asyncio.run(
            asyncio.wait_for(
                asyncio.gather(*futures.values()),
                timeout=timeout
            )
        )
    except asyncio.TimeoutError:
        self.logger.error("Task timeout")
        # Handle timeout - cancel remaining tasks
    
    return results
Chép
aggregate_results:

def aggregate_results(self, results):
    """Combine results from multiple workers"""
    aggregated = {
        "status": "success",
        "data": {},
        "code": None,
        "evaluation": None,
        "timestamp": datetime.now().isoformat()
    }
    
    for result in results:
        if result['type'] == 'data':
            aggregated['data'] = result['content']
        elif result['type'] == 'code':
            aggregated['code'] = result['content']
        # ... etc
    
    return aggregated
Chép
Test Coordinator
pytest tests/test_02_coordinator.py -v
Chép
✅ Kỳ vọng:

test_02_coordinator.py::test_coordinator_init PASSED
test_02_coordinator.py::test_parse_request PASSED
test_02_coordinator.py::test_route_task PASSED
test_02_coordinator.py::test_execute_tasks PASSED
test_02_coordinator.py::test_aggregate_results PASSED

5 passed
Chép
2.3. Cài đặt Error Handling
Hành động
Coordinator cần xử lý:

Worker timeout - worker quá lâu
Worker error - worker trả về exception
Invalid input - user input không parse được
Resource exhaustion - quá nhiều tasks
Ví dụ:

def execute_tasks_with_retry(self, tasks, max_retries=2):
    for attempt in range(max_retries):
        try:
            return self.execute_tasks(tasks, timeout=60)
        except TimeoutError:
            self.logger.warning(f"Retry {attempt+1}/{max_retries}")
            if attempt == max_retries - 1:
                raise CoordinatorException("All retries exhausted")
        except WorkerError as e:
            # One worker failed, maybe call fallback?
            self.logger.error(f"Worker error: {e}")
            # Optional: try different worker
Chép
2.4. Test End-to-End (Coordinator Only)
Hành động
Tạo mock worker agents để test coordinator in isolation:

python scripts/test_coordinator_standalone.py
Chép
✅ Output mẫu:

Testing Coordinator with mock workers...

Test 1: Simple task
  Input: "Analyze sales data"
  Parsed: task_type=data_analysis
  Routed to: data_agent
  Result: [mock data returned]
  ✓ Pass

Test 2: Multiple tasks
  Input: "Analyze AND create report"
  Routed to: data_agent, code_agent
  Results: both returned in 5.2s
  ✓ Pass

Test 3: Timeout handling
  Input: "Long task"
  Timeout after 30s
  Fallback triggered
  ✓ Pass

All coordinator tests passed! (3/3)
Chép
Kết quả mong đợi Phần 2
✅ 5 hàm coordinator cài đặt xong
✅ Error handling (timeout, exception)
✅ pytest tests/test_02_coordinator.py → 5/5 passed
✅ End-to-end test coordinator standalone → pass
⚠️ Lưu ý Phần 2
Coordinator là bottleneck
Nếu coordinator slow → toàn bộ system slow
Optimize parse_request (không call model nếu có thể regex)
Cache routing decisions
Async vs Sync
Dùng async/await để coordinator chờ workers song song
Không dùng time.sleep() (block thread)
Logging quan trọng
Log mỗi task: start, end, duration, result
Giúp debug sau này
Checklist Phần 2
 Đọc src/coordinator.py + base_agent.py
 Cài __init__: khởi tạo workers, queue, logger
 Cài parse_request: extract task type + params
 Cài route_task: xác định worker nào
 Cài execute_tasks: gửi + chờ + timeout handling
 Cài aggregate_results: kết hợp kết quả
 Error handling: timeout, exception, retry
 pytest tests/test_02_coordinator.py → passed
 Test standalone coordinator
 Commit: git add src/coordinator.py tests/ && git commit -m "part 2: coordinator implementation"


 Implement Worker Agents & Communication
Phần 3: Implement Worker Agents & Communication
Khoảng 4-5 giờ. Bạn cài đặt các worker agents (Data, Code, Evaluator), mỗi cái có tools riêng, rồi setup message queue để giao tiếp với coordinator.

Không tốn token. Mục đích: xây dựng các "nhân viên chuyên môn" của system.

3.1. Hiểu Worker Agent Pattern
Hành động
Đọc tài liệu worker agents:

cat src/agents/data_agent.py
cat src/agents/code_agent.py
cat src/agents/base_worker.py
Chép
Worker Agent cần:
Specialized tools - nó có công cụ gì?
System prompt - hướng dẫn nó làm gì?
Process method - nhận task, xử lý, return result
Error handling - nếu tool fail, làm gì?
Ví dụ 3 loại worker:
Worker	Tools	Specialty
Data Agent	SQL, pandas, DB query	Phân tích dữ liệu, truy vấn
Code Agent	Python REPL, file create/edit	Viết code, xử lý script
Evaluator	Scoring, validation	Kiểm chất lượng kết quả
3.2. Cài đặt Base Worker Class
Hành động
Mở file:

code src/agents/base_worker.py
Chép
Cài đặt base class:

class BaseWorker:
    def __init__(self, name, model, tools):
        self.name = name  # e.g., "data_agent"
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.system_prompt = None  # Subclass define
        self.logger = get_logger(name)
    
    def process(self, task_content, parameters=None):
        """Process a task synchronously"""
        try:
            # Build prompt with task
            prompt = self._build_prompt(task_content, parameters)
            
            # Call model
            response = self.model.invoke(prompt)
            
            # Process tool calls in loop (agentic loop)
            while response.tool_calls:
                tool_name = response.tool_calls[0]['name']
                tool_input = response.tool_calls[0]['input']
                
                result = self._execute_tool(tool_name, tool_input)
                
                # Continue conversation
                response = self.model.invoke(
                    prompt + f"\nTool {tool_name} returned: {result}"
                )
            
            return {
                "status": "success",
                "result": response.content,
                "metadata": {"tools_used": len(self._executed_tools)}
            }
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "result": None
            }
    
    async def process_async(self, task_content, parameters=None):
        """Process task asynchronously"""
        # Use asyncio to run process in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self.process, 
            task_content, 
            parameters
        )
    
    def _build_prompt(self, task_content, parameters):
        """Build full prompt with system instructions"""
        return f"""
{self.system_prompt}

Task: {task_content}
Parameters: {parameters or {}}

Available tools: {list(self.tools.keys())}
"""
    
    def _execute_tool(self, tool_name, tool_input):
        """Execute a tool and return result"""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool = self.tools[tool_name]
        try:
            result = tool.invoke(tool_input)
            self._executed_tools.append(tool_name)
            return result
        except Exception as e:
            self.logger.error(f"Tool {tool_name} failed: {e}")
            raise
Chép
3.3. Cài đặt Specialized Workers
Hành động
code src/agents/data_agent.py
code src/agents/code_agent.py
code src/agents/evaluator_agent.py
Chép
Data Agent
class DataAgent(BaseWorker):
    def __init__(self, model, db_connection=None):
        tools = [
            QueryDatabaseTool(db_connection),
            PandasAnalysisTool(),
            CSVParserTool(),
            DataValidationTool()
        ]
        super().__init__("data_agent", model, tools)
        
        self.system_prompt = """
You are a Data Analysis Specialist. Your job:
1. Analyze data queries from coordinator
2. Use SQL tools to query databases
3. Use pandas to process data
4. Return insights, not raw data

When coordinator asks "analyze sales", you:
- Query SQL for data
- Calculate aggregates (sum, avg, group_by)
- Return formatted insights: "Sales: $5M, +10% MoM"

Available tools:
- query_database: "SELECT ... FROM ..."
- pandas_analysis: "df.groupby(...).sum()"
"""

class CodeAgent(BaseWorker):
    def __init__(self, model):
        tools = [
            PythonREPLTool(),
            CreateFileTool(),
            EditFileTool(),
            RunScriptTool()
        ]
        super().__init__("code_agent", model, tools)
        
        self.system_prompt = """
You are a Code Generation Specialist. Your job:
1. Write Python code to solve tasks
2. Test code locally with REPL
3. Create/edit files if needed
4. Return working code + output

When coordinator asks "create report", you:
- Write Python script using pandas, matplotlib
- Run REPL to test
- Return path to report file + console output

Important: ALWAYS test code before returning!
"""

class EvaluatorAgent(BaseWorker):
    def __init__(self, model):
        tools = [
            ScoringTool(),
            ValidationTool(),
            QualityCheckTool(),
            FeedbackGeneratorTool()
        ]
        super().__init__("evaluator_agent", model, tools)
        
        self.system_prompt = """
You are a Quality Evaluation Specialist. Your job:
1. Evaluate results from data/code agents
2. Score on accuracy, completeness, clarity
3. Identify issues
4. Suggest improvements

Evaluation criteria:
- Accuracy: 30% (correctness)
- Completeness: 30% (all requirements met)
- Clarity: 20% (easy to understand)
- Performance: 20% (efficient)

Return format:
{
  "score": 0-100,
  "feedback": "What's good/bad",
  "issues": ["issue1", "issue2"],
  "suggestions": ["fix1", "fix2"]
}
"""
Chép
Test Workers
pytest tests/test_03_workers.py -v
Chép
✅ Kỳ vọng:

test_03_workers.py::test_data_agent_init PASSED
test_03_workers.py::test_data_agent_process PASSED
test_03_workers.py::test_code_agent_process PASSED
test_03_workers.py::test_evaluator_agent PASSED

4 passed
Chép
3.4. Cài đặt Message Queue & Communication
Hành động
code src/communication/message_queue.py
Chép
Implement message queue (có thể dùng asyncio.Queue hoặc thư viện khác):

class MessageQueue:
    """Simple in-memory message queue for agent communication"""
    
    def __init__(self):
        self.queues = {}  # {agent_name: asyncio.Queue}
        self.message_log = []  # Log tất cả messages
    
    def register_agent(self, agent_name):
        """Register an agent to receive messages"""
        self.queues[agent_name] = asyncio.Queue()
    
    async def send_message(self, from_agent, to_agent, message):
        """Send message from one agent to another"""
        if to_agent not in self.queues:
            raise ValueError(f"Agent {to_agent} not registered")
        
        # Add metadata
        message['from'] = from_agent
        message['to'] = to_agent
        message['timestamp'] = datetime.now().isoformat()
        message['id'] = str(uuid.uuid4())
        
        # Log message
        self.message_log.append(message)
        
        # Enqueue
        await self.queues[to_agent].put(message)
        
        return message['id']
    
    async def receive_message(self, agent_name, timeout=30):
        """Receive next message for an agent"""
        try:
            message = await asyncio.wait_for(
                self.queues[agent_name].get(),
                timeout=timeout
            )
            return message
        except asyncio.TimeoutError:
            raise TimeoutError(f"No message for {agent_name} within {timeout}s")
    
    def get_message_log(self, agent_name=None):
        """Get message history"""
        if agent_name:
            return [m for m in self.message_log 
                   if m['from'] == agent_name or m['to'] == agent_name]
        return self.message_log
Chép
3.5. Integrate Workers + Communication
Hành động
Sửa coordinator để dùng message queue:

# src/coordinator.py - modified execute_tasks

async def execute_tasks(self, tasks, message_queue):
    """Execute tasks via message queue"""
    futures = []
    
    for task in tasks:
        # Send task to worker via message queue
        msg_id = await message_queue.send_message(
            from_agent="coordinator",
            to_agent=task['worker'],
            message={
                "type": "task",
                "task_id": task['id'],
                "content": task['content'],
                "parameters": task.get('parameters', {})
            }
        )
        
        # Create listener coroutine
        async def listen_for_result(worker_name):
            try:
                result = await message_queue.receive_message(
                    "coordinator",
                    timeout=60
                )
                return result
            except TimeoutError:
                return {"status": "timeout", "worker": worker_name}
        
        futures.append(listen_for_result(task['worker']))
    
    # Wait for all results
    results = await asyncio.gather(*futures)
    return results
Chép
Kết quả mong đợi Phần 3
✅ Base Worker class cài đặt xong
✅ 3 specialized workers: Data, Code, Evaluator
✅ System prompt rõ ràng cho mỗi worker
✅ Message queue implementation
✅ Communication dùng async/await
✅ pytest tests/test_03_workers.py → 4/4 passed
⚠️ Lưu ý Phần 3
Tool Execution Safety
Sandbox Python REPL nếu dùng code_agent
Validate SQL queries trước execute
Set resource limits (timeout, memory)
Message Logging
Log tất cả communication để debug
JSON format dễ parse
Giúp trace issue sau
Async Best Practices
Dùng asyncio.gather() để chạy parallel
Luôn set timeout để tránh hang
Handle exception từ workers gracefully
Checklist Phần 3
 Đọc base_worker.py + agent files
 Cài BaseWorker class: process, process_async, _build_prompt, _execute_tool
 Cài DataAgent: tools, system_prompt
 Cài CodeAgent: tools, system_prompt, sandbox setup
 Cài EvaluatorAgent: tools, system_prompt, scoring
 Cài MessageQueue: send_message, receive_message, logging
 Integrate MessageQueue với Coordinator
 pytest tests/test_03_workers.py → passed
 Test communication: coordinator ↔ worker
 Commit: git add src/agents/ src/communication/ && git commit -m "part 3: workers and communication"


 Tích hợp Tools & Hợp tác Agent
Phần 4: Tích hợp Tools & Hợp tác Agent
Khoảng 4-5 giờ. Bạn cài đặt các tools chuyên biệt cho mỗi worker, setup environment (database connection, Python sandbox), và test collaboration giữa các agents.

Không tốn token (chỉ local execution). Mục đích: làm cho các worker hoạt động được.

4.1. Thiết kế Tool Architecture
Hành động
Đọc tài liệu tools:

cat src/tools/base_tool.py
ls -la src/tools/
Chép
Tool cần có:
class BaseTool:
    """Base class cho tất cả tools"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description  # LLM dùng để hiểu
    
    def invoke(self, input_dict):
        """Execute tool with input"""
        raise NotImplementedError
    
    def validate_input(self, input_dict):
        """Validate input before execution"""
        raise NotImplementedError
Chép
Tools cần cho từng worker:
Data Agent Tools:

QueryDatabaseTool - Chạy SQL query
PandasTool - Phân tích data với pandas
CSVParserTool - Parse CSV files
AggregationTool - Tính aggregates
Code Agent Tools:

PythonREPLTool - Thực thi Python code
CreateFileTool - Tạo file
EditFileTool - Sửa file
RunScriptTool - Chạy script Python
Evaluator Agent Tools:

ScoringTool - Chấm điểm (0-100)
ValidationTool - Kiểm tra format
ComparisonTool - So sánh results
ReportGeneratorTool - Tạo báo cáo
4.2. Cài đặt Database Connection (Data Agent)
Hành động
code src/tools/database_tools.py
Chép
Implement QueryDatabaseTool:

class QueryDatabaseTool(BaseTool):
    def __init__(self, connection_string):
        super().__init__(
            name="query_database",
            description="Execute SQL queries on the connected database"
        )
        self.conn_string = connection_string
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        import sqlite3  # Hoặc psycopg2, pymysql, etc.
        self.connection = sqlite3.connect(self.conn_string)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def validate_input(self, input_dict):
        """Validate SQL query"""
        query = input_dict.get('query', '')
        
        # Check for dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER']
        for keyword in dangerous_keywords:
            if keyword in query.upper():
                raise ValueError(f"Dangerous operation: {keyword} not allowed")
        
        # Check for basic SQL syntax
        if not query.upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries allowed")
        
        return True
    
    def invoke(self, input_dict):
        """Execute query and return results"""
        try:
            self.validate_input(input_dict)
            
            if not self.connection:
                self.connect()
            
            query = input_dict['query']
            limit = input_dict.get('limit', 1000)
            
            # Add LIMIT to prevent huge result sets
            query_with_limit = f"{query} LIMIT {limit}"
            
            cursor = self.connection.cursor()
            cursor.execute(query_with_limit)
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            return {
                "status": "success",
                "rows": len(rows),
                "columns": columns,
                "data": [dict(row) for row in rows[:100]]  # Return first 100 rows
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
Chép
4.3. Cài đặt Python Sandbox (Code Agent)
Hành động
code src/tools/code_tools.py
Chép
Implement PythonREPLTool với safety:

import sys
import io
from contextlib import redirect_stdout, redirect_stderr

class PythonREPLTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="python_repl",
            description="Execute Python code in a sandboxed environment"
        )
        self.globals = {}
        self.max_output_len = 10000  # Limit output size
    
    def validate_input(self, input_dict):
        """Validate Python code"""
        code = input_dict.get('code', '')
        
        # Check for dangerous imports
        dangerous_imports = ['os', 'subprocess', 'shutil', 'sys']
        for imp in dangerous_imports:
            if f'import {imp}' in code or f'from {imp}' in code:
                # Allow some safe modules
                if imp not in ['sys']:  # sys.version ok, but not sys.exit
                    raise ValueError(f"Import {imp} not allowed")
        
        return True
    
    def invoke(self, input_dict):
        """Execute Python code"""
        try:
            self.validate_input(input_dict)
            
            code = input_dict['code']
            
            # Capture output
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                try:
                    # Execute with timeout
                    exec(code, self.globals)
                except Exception as e:
                    return {
                        "status": "error",
                        "error": str(e),
                        "type": type(e).__name__
                    }
            
            stdout = output_buffer.getvalue()[:self.max_output_len]
            stderr = error_buffer.getvalue()[:self.max_output_len]
            
            return {
                "status": "success",
                "stdout": stdout,
                "stderr": stderr,
                "variables": {k: str(v) for k, v in self.globals.items() 
                            if not k.startswith('_')}
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

class CreateFileTool(BaseTool):
    def __init__(self, base_path="./outputs"):
        super().__init__(
            name="create_file",
            description="Create a new file with content"
        )
        self.base_path = base_path
    
    def validate_input(self, input_dict):
        """Validate file path (no path traversal)"""
        filename = input_dict.get('filename', '')
        
        # Prevent path traversal
        if '..' in filename or filename.startswith('/'):
            raise ValueError("Invalid filename")
        
        return True
    
    def invoke(self, input_dict):
        """Create file"""
        try:
            self.validate_input(input_dict)
            
            filename = input_dict['filename']
            content = input_dict['content']
            
            filepath = f"{self.base_path}/{filename}"
            
            # Create directory if needed
            import os
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            return {
                "status": "success",
                "path": filepath,
                "size": len(content)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
Chép
4.4. Cài đặt Evaluation Tools (Evaluator Agent)
Hành động
code src/tools/evaluation_tools.py
Chép
Implement ScoringTool:

class ScoringTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="score_result",
            description="Score a result on various criteria"
        )
    
    def invoke(self, input_dict):
        """Score result based on criteria"""
        result = input_dict.get('result', '')
        criteria = input_dict.get('criteria', {})
        # Format: {"accuracy": 30, "completeness": 30, "clarity": 20, "performance": 20}
        
        scores = {}
        total_weight = sum(criteria.values())
        
        # TODO: Implement actual scoring logic
        # This could call another LLM to evaluate or use heuristics
        
        # Simple heuristic example:
        if result:
            scores['accuracy'] = min(100, len(result) * 2)  # Placeholder
            scores['completeness'] = 80 if len(result) > 100 else 40
            scores['clarity'] = 75 if '\n' in result else 50
            scores['performance'] = 90
        
        weighted_score = sum(
            scores.get(criterion, 0) * weight / total_weight
            for criterion, weight in criteria.items()
        )
        
        return {
            "status": "success",
            "scores": scores,
            "weighted_score": round(weighted_score, 2),
            "grade": self._score_to_grade(weighted_score)
        }
    
    def _score_to_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        if score >= 60: return "D"
        return "F"
Chép
4.5. Test Tool Integration
Hành động
Test từng tool individually:

pytest tests/test_04_tools.py -v
Chép
✅ Kỳ vọng:

test_04_tools.py::test_query_database_tool PASSED
test_04_tools.py::test_python_repl_tool PASSED
test_04_tools.py::test_create_file_tool PASSED
test_04_tools.py::test_scoring_tool PASSED

4 passed
Chép
Test tool collaboration (worker dùng tool):

python scripts/test_tool_integration.py
Chép
✅ Output mẫu:

Test: Data Agent queries database
  ├─ SQL: "SELECT * FROM sales WHERE year=2026"
  └─ Result: 50 rows returned ✓

Test: Code Agent creates visualization
  ├─ Python code: imports matplotlib + creates plot
  ├─ REPL: executed successfully
  └─ File created: outputs/sales_chart.png ✓

Test: Evaluator scores the result
  ├─ Accuracy: 85/100
  ├─ Completeness: 90/100
  ├─ Clarity: 80/100
  └─ Overall: 85/100 (B) ✓

All tool tests passed! (3/3)
Chép
Kết quả mong đợi Phần 4
✅ Database connection setup (QueryDatabaseTool)
✅ Python sandbox (PythonREPLTool, CreateFileTool)
✅ Evaluation tools (ScoringTool, ValidationTool)
✅ All tools have proper input validation
✅ pytest tests/test_04_tools.py → 4/4 passed
✅ Tool integration test → pass
⚠️ Lưu ý Phần 4
Security First
Query validation: nếu dùng real database, cần strict SQL validation
Code sandbox: dùng RestrictedPython hoặc container nếu cần safer execution
File operations: limit path, prevent directory traversal
Resource limits: set timeout, memory limit trên REPL
Performance
Cache database connections (không reconnect mỗi query)
Limit query result size (LIMIT 1000)
Timeout on long-running code (default 30s)
Logging
Log tất cả tool executions (query, code, error)
Track execution time
Capture stdout/stderr
Checklist Phần 4
 Đọc base_tool.py + tool files
 Cài QueryDatabaseTool: connection, validate, invoke
 Cài PythonREPLTool: sandbox, validate, timeout
 Cài CreateFileTool: path validation, file creation
 Cài ScoringTool: scoring logic, grading
 Cài ValidationTool (nếu cần)
 Setup database connection (test database)
 Setup Python sandbox with safety
 pytest tests/test_04_tools.py → passed
 Test tool integration end-to-end
 Commit: git add src/tools/ && git commit -m "part 4: tools integration"


 Test, Debug & Đánh giá Hiệu suất
Phần 5: Test, Debug & Đánh giá Hiệu suất
Khoảng 4-5 giờ. Bạn viết test cases, chạy end-to-end system, phân tích logs, tìm bottlenecks, và đo hiệu suất.

Tốn token (gọi LLM). Mục đích: đảm bảo system hoạt động ổn định.

5.1. Viết Test Cases
Hành động
cat tests/test_05_integration.py
# Xem structure các test case
Chép
Loại test cần:
Unit tests - từng component (coordinator, worker, tool)
Integration tests - coordinator ↔ worker ↔ tool
End-to-end tests - user request → final response
Performance tests - latency, throughput
Ví dụ test structure:
import pytest
import asyncio

# Unit test
def test_coordinator_parse_request():
    coord = Coordinator(model)
    result = coord.parse_request("Analyze sales data")
    
    assert result['task_type'] == "data_analysis"
    assert result['parameters'] is not None

# Integration test
@pytest.mark.asyncio
async def test_coordinator_with_workers():
    coordinator = Coordinator(model, workers=[data_agent, code_agent])
    
    request = "Calculate revenue and create chart"
    response = await coordinator.handle_request(request)
    
    assert response['status'] == 'success'
    assert 'data' in response
    assert 'code' in response

# End-to-end test
@pytest.mark.asyncio
async def test_full_pipeline():
    system = MultiAgentSystem(
        coordinator=coordinator,
        workers=[data_agent, code_agent, evaluator]
    )
    
    # Simulate user input
    user_input = "What was Q3 revenue? Create a visualization."
    
    # Process through full system
    result = await system.process(user_input)
    
    # Verify result
    assert result['status'] == 'success'
    assert 'revenue' in result['data'].lower() or '5' in result['data']
    assert 'chart' in result['code'] or 'plot' in result['code']
    assert 'score' in result['evaluation']

# Performance test
@pytest.mark.asyncio
async def test_latency():
    import time
    
    system = MultiAgentSystem(...)
    request = "Simple task"
    
    start = time.time()
    result = await system.process(request)
    latency = time.time() - start
    
    assert latency < 10  # Should finish in 10 seconds
    print(f"Latency: {latency:.2f}s")

# Stress test
@pytest.mark.asyncio
async def test_concurrent_requests():
    system = MultiAgentSystem(...)
    
    # Send 10 concurrent requests
    tasks = [
        system.process(f"Task {i}")
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    assert success_count >= 8  # At least 80% success
Chép
Run tests
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_05_integration.py -v

# With performance metrics
pytest tests/ --durations=10  # Show 10 slowest tests
Chép
5.2. Debug Multi-Agent System
Hành động
Khi system không work, debug bằng:

# 1. Check coordinator logs
tail -f logs/coordinator.log

# 2. Check communication logs
cat logs/communication.log | jq .  # Pretty print JSON

# 3. Check worker logs
tail -f logs/data_agent.log

# 4. Run specific agent standalone
python scripts/debug_agent.py --agent data_agent --task "SELECT * FROM sales"

# 5. Enable debug logging
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from src.system import MultiAgentSystem
system = MultiAgentSystem(...)
"
Chép
Common issues & solutions:
Issue	Dấu hiệu	Giải pháp
Coordinator timeout	"TimeoutError after 60s"	↑ timeout, check if worker hung
Worker crash	Worker logs show exception	Run worker test standalone
Message queue full	"Queue.full()"	Increase queue size or process faster
Tool execution fail	"Database connection refused"	Check DB connection, credentials
LLM rate limit	"RateLimitError"	Add exponential backoff retry
Debug script example:
code scripts/debug_system.py
Chép
import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def debug_request(request):
    """Debug single request with full logging"""
    system = MultiAgentSystem(...)
    
    print(f"🔍 Debugging: {request}")
    print("-" * 50)
    
    try:
        result = await system.process(request, debug=True)
        
        print("\n✅ Success!")
        print(f"Status: {result['status']}")
        print(f"Data: {result.get('data', 'N/A')[:200]}")
        print(f"Evaluation: {result.get('evaluation', 'N/A')}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Run debug
if __name__ == "__main__":
    request = "Analyze Q3 sales and create report"
    asyncio.run(debug_request(request))
Chép
5.3. Performance Profiling
Hành động
code scripts/profile_system.py
Chép
import cProfile
import pstats
import asyncio

async def run_system():
    system = MultiAgentSystem(...)
    for i in range(5):
        await system.process(f"Test request {i}")

# Profile
profiler = cProfile.Profile()
profiler.enable()

asyncio.run(run_system())

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest functions
Chép
Performance metrics to track:
Metric	Target	How to measure
Latency (P50)	< 5s	time.time()
Latency (P99)	< 15s	percentile(latencies)
Throughput	> 10 req/min	requests/minute
Worker utilization	70-90%	time spent processing / total time
Error rate	< 1%	failed / total
Token usage	150k/100 req	count API tokens
5.4. Benchmarking
Hành động
Tạo benchmark suite:

code scripts/benchmark.py
Chép
import asyncio
import time
import json

class Benchmark:
    def __init__(self):
        self.results = []
    
    async def run_test(self, name, request, system, iterations=3):
        """Run benchmark test multiple times"""
        print(f"\n📊 Benchmarking: {name}")
        
        latencies = []
        
        for i in range(iterations):
            start = time.time()
            result = await system.process(request)
            latency = time.time() - start
            
            latencies.append(latency)
            status = "✓" if result['status'] == 'success' else "✗"
            print(f"  Iteration {i+1}: {latency:.2f}s {status}")
        
        # Calculate stats
        stats = {
            "name": name,
            "iterations": iterations,
            "min": min(latencies),
            "max": max(latencies),
            "avg": sum(latencies) / len(latencies),
            "median": sorted(latencies)[len(latencies)//2]
        }
        
        self.results.append(stats)
        
        print(f"  Summary:")
        print(f"    Min: {stats['min']:.2f}s")
        print(f"    Max: {stats['max']:.2f}s")
        print(f"    Avg: {stats['avg']:.2f}s")
        print(f"    Median: {stats['median']:.2f}s")
        
        return stats

# Run benchmarks
async def main():
    system = MultiAgentSystem(...)
    bench = Benchmark()
    
    # Test cases
    test_cases = [
        ("Simple data query", "What is total revenue?"),
        ("Code generation", "Write Python script to read CSV"),
        ("Complex workflow", "Analyze sales data AND create chart AND evaluate result"),
    ]
    
    for name, request in test_cases:
        await bench.run_test(name, request, system)
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        json.dump(bench.results, f, indent=2)
    
    print("\n✅ Benchmark complete. Results saved to benchmark_results.json")

asyncio.run(main())
Chép
Run benchmark
python scripts/benchmark.py
# Output: benchmark_results.json
Chép
5.5. Ghi kết quả vào báo cáo
Hành động
Ghi vào report/REPORT.md mục 5-6:

## Mục 5: Test Results

### Unit Tests
- Coordinator: 5/5 passed ✓
- Workers: 3/3 passed ✓
- Tools: 4/4 passed ✓

### Integration Tests
- Coordinator + Workers: 2/2 passed ✓
- Full Pipeline: 1/1 passed ✓

### Total: 15/15 tests passed ✓

---

## Mục 6: Performance Analysis

### Benchmark Results

| Test Case | Min | Max | Avg | Median |
|-----------|-----|-----|-----|--------|
| Simple query | 1.2s | 1.8s | 1.5s | 1.5s |
| Code gen | 3.1s | 4.2s | 3.6s | 3.5s |
| Complex workflow | 6.5s | 8.2s | 7.3s | 7.2s |

### Performance Metrics

- **Latency (P50)**: 3.6s ✓ (target: < 5s)
- **Latency (P99)**: 8.2s ✓ (target: < 15s)
- **Throughput**: 8 req/min (limited by model API)
- **Error rate**: 0% ✓
- **Token usage**: 150k tokens / 100 requests

### Findings

1. **Bottleneck**: Code Agent slower than expected (3.6s avg)
   - Reason: Python REPL startup time
   - Solution: Pre-warm Python environment

2. **Success**: All tests passed, no errors
   - System stable under load
   - Message queue working smoothly

3. **Optimization opportunity**:
   - Coordinator parsing could cache decisions
   - Worker response time could improve with parallel tool execution
Chép
Kết quả mong đợi Phần 5
✅ Test suite với unit + integration + e2e tests
✅ All tests pass: pytest tests/ -v → all passed
✅ Debug tools & scripts
✅ Benchmark suite with performance metrics
✅ Logs collected & analyzed
✅ Mục 5-6 báo cáo có metrics
⚠️ Lưu ý Phần 5
Test Coverage
Aim for > 80% code coverage
Test both happy path + error cases
Test edge cases (empty input, timeout, etc.)
Async Testing
Use @pytest.mark.asyncio decorator
Use asyncio.gather() for concurrent tests
Always set timeout on async operations
Logging is Key
Detailed logs help debug issues
JSON format easier to parse
Save logs from each test run
Checklist Phần 5
 Viết unit tests cho coordinator, workers, tools
 Viết integration tests (coordinator ↔ worker)
 Viết e2e tests (full pipeline)
 pytest tests/ -v → all passed
 Create debug scripts
 Debug common issues + document solutions
 Run performance profiling
 Create benchmark suite
 Run benchmarks 3+ times
 Analyze results + identify bottlenecks
 Ghi kết quả vào báo cáo mục 5-6
 Commit: git add tests/ scripts/ benchmark_results.json report/ && git commit -m "part 5: testing and benchmarking"


 Checklist Nộp bài
Phần 6: Báo cáo & Thử thách Mở rộng
Khoảng 3-4 giờ. Bạn viết báo cáo toàn diện, tóm tắt thiết kế, kết quả test, phân tích hiệu suất. Bonus: thêm các tính năng nâng cao (+5 điểm).

Nội dung Báo cáo Bắt buộc (10 mục)
Mục 1: Tổng quan Bài Lab
Nội dung: Mô tả bài toán, goal, scope.

Ví dụ:

Bài lab này xây dựng một hệ thống multi-agent orchestration để xử lý các task phức tạp
yêu cầu collaboration giữa các specialized agents:

- **Coordinator Agent**: Nhận user request, phân tích task type, định tuyến đến workers
- **Data Agent**: Xử lý data queries (SQL, pandas analysis)
- **Code Agent**: Tạo scripts, chạy Python code
- **Evaluator Agent**: Kiểm chất lượng kết quả, cho feedback

Mục tiêu: Xây dựng system stable, efficient, và scalable để handle multiple request types.
Chép
Mục 2: Kiến trúc Design
Nội dung: Sơ đồ + mô tả các component.

Yêu cầu:

Sơ đồ kiến trúc (từ Phần 1)
Mô tả mỗi component
Message flow diagram
Communication protocol
Ví dụ:

## Kiến trúc Tổng quát

[INSERT ARCHITECTURE DIAGRAM]

### Components

1. **Coordinator**: Central hub
   - Nhận user request (string)
   - Parse → extract task type + params
   - Route → send to 1 hoặc multiple workers
   - Aggregate → combine results
   - Return → formatted response

2. **Workers**: Specialized agents
   - Data Agent: DB queries + data analysis
   - Code Agent: Python code generation + execution
   - Evaluator: Quality scoring + feedback

3. **Tools**: Shared utilities
   - Query Tool: SQL execution
   - REPL Tool: Python sandbox
   - File Tool: Create/edit files
   - Scoring Tool: Evaluate results

### Communication

```json
{
  "type": "task_request",
  "from": "coordinator",
  "to": "data_agent",
  "content": "Analyze Q3 sales",
  "timeout": 60
}
Chép
Coordinator → Worker via async message queue (30s timeout, 3 retries)


### Mục 3: Implementation Details

**Nội dung:** Cách bạn cài đặt từng component.

**Yêu cầu:**
- Highlight những quyết định thiết kế
- Trade-offs
- Challenges & solutions

**Ví dụ:**
```markdown
## Implementation Decisions

### 1. Async Architecture
- **Decision**: Dùng asyncio thay vì threading
- **Reason**: Python GIL, better for I/O-bound operations
- **Trade-off**: Complexity tăng, debugging khó hơn

### 2. In-memory Message Queue
- **Decision**: asyncio.Queue thay vì external message broker
- **Reason**: Lab scope nhỏ, simplicity
- **Trade-off**: Không persistent, single-process only

### 3. Python Sandbox (REPL)
- **Decision**: Restrict exec() scope, no system imports
- **Reason**: Safety against malicious code
- **Trade-off**: Limited functionality (no file I/O, subprocess)

### 4. Database Connection Pooling
- **Decision**: Cache connection, reuse across queries
- **Reason**: Performance (avoid reconnect overhead)
- **Trade-off**: Resource management (need close gracefully)
Chép
Mục 4: Test Results
Nội dung: Test suite results + coverage.

Yêu cầu:

Unit test results
Integration test results
E2E test results
Error cases handled
Ví dụ:

## Test Coverage

### Unit Tests (15 tests)
- Coordinator: 5/5 ✓
- Workers: 3/3 ✓
- Tools: 4/4 ✓
- Communication: 3/3 ✓

### Integration Tests (5 tests)
- Coordinator ↔ Data Agent: 2/2 ✓
- Coordinator ↔ Code Agent: 2/2 ✓
- Message Queue: 1/1 ✓

### End-to-End Tests (3 tests)
- Simple query: PASSED ✓
- Complex workflow: PASSED ✓
- Error handling: PASSED ✓

**Total: 23/23 tests passed**

### Test Cases

| Test | Scenario | Result |
|------|----------|--------|
| `test_coordinator_simple` | "Analyze sales" | ✓ |
| `test_coordinator_complex` | "Analyze + create chart + evaluate" | ✓ |
| `test_worker_timeout` | Worker không respond sau 30s | ✓ (graceful timeout) |
| `test_message_loss` | Message queue full | ✓ (error returned) |
| `test_sql_injection` | SQL: "SELECT * FROM users; DROP TABLE" | ✓ (blocked) |
Chép
Mục 5: Performance Analysis
Nội dung: Benchmark results + bottleneck analysis.

Yêu cầu:

Latency metrics (P50, P99)
Throughput
Resource usage
Bottleneck identification
Ví dụ:

## Performance Benchmarks

### Latency Results

| Scenario | Min | Max | Avg | Median |
|----------|-----|-----|-----|--------|
| Simple query | 1.2s | 1.8s | 1.5s | 1.5s |
| Code generation | 3.1s | 4.2s | 3.6s | 3.5s |
| Complex workflow | 6.5s | 8.2s | 7.3s | 7.2s |

### Throughput
- Single request: 1.5s average
- Sustained throughput: 40 requests/hour (7 req/min)
- Bottleneck: OpenAI API rate limit, not system design

### Resource Usage
- Memory: ~50MB baseline, +10MB per concurrent request
- CPU: Low utilization (mostly waiting on I/O)
- Connections: 1 DB connection cached, reused

### Bottleneck Analysis

**Identified Issue 1: Code Agent Slow**
- Symptom: Code generation takes 3.6s vs Data 1.5s
- Root cause: Python REPL startup + LLM inference
- Solution: Pre-warm Python environment, cache model
- Impact: Could save ~500ms per request

**Identified Issue 2: Message Queue Throughput**
- Current: 7 req/min
- Bottleneck: LLM API (gpt-4o-mini concurrent limit)
- Solution: Async request batching, model caching
- Impact: Not system architecture issue

### Optimization Recommendations
1. Pre-warm Python interpreter (500ms saving)
2. Cache coordinator parsing decisions (100ms saving)
3. Implement worker result caching (variable)
4. Add request prioritization (QoS improvement)
Chép
Mục 6: Error Analysis & Resilience
Nội dung: Cách system xử lý lỗi, edge cases.

Yêu cầu:

Error types encountered
How handled
Resilience mechanisms
Ví dụ:

## Error Handling Strategy

### 1. Timeout Errors
- **Detection**: asyncio.TimeoutError
- **Handling**: Retry up to 3 times, exponential backoff
- **Fallback**: Return partial result or error message
- **Test**: test_worker_timeout ✓

### 2. Tool Execution Errors
- **Detection**: Exception in tool.invoke()
- **Handling**: Catch, log, return error to worker
- **Worker**: Try different tool or report to coordinator
- **Test**: test_sql_injection, test_python_sandbox ✓

### 3. Message Queue Errors
- **Detection**: Queue full, message drop
- **Handling**: Drop oldest message, warn in logs
- **Coordinator**: Retry worker immediately
- **Test**: test_queue_overflow ✓

### 4. Graceful Degradation
- If one worker fails: try alternative worker
- If no alternative: return partial result
- If critical error: report to user

### Resilience Score: 8/10
- Good error detection + handling
- Minor: Không có circuit breaker pattern
- Minor: Không có manual recovery interface
Chép
Mục 7: Comparison: Design vs Implementation
Nội dung: Bạn dự kiến gì ở Phần 1, kết quả thực tế như thế nào?

Ví dụ:

## Design vs Reality

| Aspect | Planned | Actual | Difference |
|--------|---------|--------|-----------|
| Latency | < 5s | 1.5-7.3s | ✓ Met |
| Throughput | 10 req/min | 7 req/min | API limit, not system |
| Error rate | < 1% | 0.5% | ✓ Better |
| Test coverage | 80% | 95% | ✓ Better |

### What went well
- Message queue architecture simple + effective
- Async/await handling smooth
- Tool safety mechanisms work

### What was hard
- Debugging async code (tricky to trace)
- Python sandbox restrictions (limited features)
- Communication protocol versioning (breaking changes)

### Lessons learned
1. Start with simple design, add complexity as needed
2. Logging is essential for async systems
3. Message format should be versioned from day 1
Chép
Mục 8: Scalability Analysis
Nội dung: Nếu scale up (more agents, more workers), system sẽ làm gì?

Ví dụ:

## Scalability Considerations

### Horizontal Scaling (More Workers)
- **Current**: 1 coordinator, 3 workers
- **Bottleneck**: Coordinator becomes single point of failure
- **Solution**: Load-balance coordinators, use external message broker (RabbitMQ)
- **Feasibility**: Medium (need Redis/RabbitMQ)

### Vertical Scaling (Larger Tasks)
- **Current**: Max query result = 1000 rows
- **Limit**: Memory, no streaming
- **Solution**: Stream results, implement pagination
- **Feasibility**: Easy (add generator-based response)

### Request Throughput
- **Current**: 7 req/min (API limited)
- **Limit**: LLM API rate limit (100 req/min for gpt-4o-mini)
- **Solution**: Use faster model (gpt-3.5), local LLM
- **Feasibility**: Easy (swap model)

### Scalability Score: 6/10
- Message queue not persistent (single process only)
- Coordinator not fault-tolerant
- Workers can scale independently ✓
Chép
Mục 9: Hạn chế & Cân nhắc
Nội dung: Thừa nhận giới hạn.

Ví dụ:

## Limitations

1. **Single Process Only**
   - In-memory queue không distributed
   - Can't run on multiple machines
   - Mitigation: Use external message broker

2. **No Persistent State**
   - Results lost if process crashes
   - No audit trail of requests
   - Mitigation: Add database logging

3. **Python Sandbox Limited**
   - Can't do file I/O, system calls
   - Can't import most packages
   - Mitigation: Use container-based execution (Docker)

4. **Synchronous Tool Calls**
   - Database queries block coordinator
   - No parallel tool execution within worker
   - Mitigation: Implement async tool execution

5. **Fixed Timeout**
   - 30s timeout may be too short/long
   - Mitigation: Make timeout configurable per task type
Chép
Mục 10: Kết luận & Đề xuất Tiếp theo
Nội dung: Summary + future work.

Ví dụ:

## Conclusion

Đã xây dựng thành công một hệ thống multi-agent orchestration:
- ✓ 4 agents hoạt động ổn định
- ✓ 23/23 tests pass
- ✓ Latency < 7.5s cho complex workflows
- ✓ Error handling + resilience mechanisms

System architecture phù hợp cho lab scope nhỏ nhưng cần scale up để production.

## Recommended Next Steps

1. **Short term (1-2 days)**
   - Add persistent logging (database)
   - Implement circuit breaker pattern
   - Add request priority queue

2. **Medium term (1 week)**
   - Switch to distributed message broker (Redis)
   - Add coordinator replication (fault tolerance)
   - Implement caching layer

3. **Long term (2-4 weeks)**
   - Migrate to cloud (AWS, GCP)
   - Add monitoring + alerting
   - Implement auto-scaling

## Final Score: 9/10
- Architecture: 9/10 (clean, modular)
- Implementation: 8/10 (solid, some improvements possible)
- Testing: 10/10 (comprehensive coverage)
- Performance: 8/10 (good, could optimize further)
- Documentation: 9/10 (clear, detailed)
Chép
Bonus Challenges (+5 điểm)
Chọn một hướng để tăng điểm:

Hướng 6a: Implement Agent Pooling
Idea: Thay vì 1 coordinator, dùng 3 coordinators chạy song song, load-balanced.

Cài đặt:

class CoordinatorPool:
    def __init__(self, num_coordinators=3):
        self.coordinators = [
            Coordinator(...) for _ in range(num_coordinators)
        ]
        self.current_index = 0
    
    async def handle_request(self, request):
        """Round-robin distribute requests"""
        coordinator = self.coordinators[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.coordinators)
        return await coordinator.handle_request(request)
Chép
Ghi vào báo cáo:

## Phụ lục: 6a - Coordinator Pooling

- Implemented 3 coordinators with round-robin load balancing
- Throughput: 7 req/min → 15 req/min (+114%)
- Latency: No significant increase
- Failover: If 1 coordinator fails, other 2 still work ✓
Chép
Hướng 6b: Implement Worker Fallback
Idea: Nếu data_agent fail, try code_agent hoặc evaluator thay vì fail ngay.

Cài đặt:

async def execute_with_fallback(self, primary_worker, fallback_workers, task):
    for worker in [primary_worker] + fallback_workers:
        try:
            return await worker.process_async(task, timeout=30)
        except Exception as e:
            logger.warning(f"{worker.name} failed, trying next")
    
    raise Exception("All workers failed")
Chép
Hướng 6c: Implement Result Caching
Idea: Cache results từ frequent tasks để avoid redundant computation.

Cài đặt:

from functools import lru_cache

class CachingCoordinator:
    def __init__(self):
        self.cache = {}  # {request_hash: result}
    
    async def handle_request(self, request):
        request_hash = hash(request)
        
        if request_hash in self.cache:
            logger.info(f"Cache hit for: {request}")
            return self.cache[request_hash]
        
        result = await super().handle_request(request)
        self.cache[request_hash] = result
        
        return result
Chép
Hướng 6d: Implement Dynamic Routing
Idea: Coordinator learns từ past results, optimize routing decisions.

Cài đặt:

class SmartCoordinator:
    def __init__(self):
        self.routing_stats = {
            "data_query": {},  # {worker: success_rate}
            "code_gen": {},
        }
    
    def route_task(self, task_type):
        """Route to best-performing worker for this task type"""
        stats = self.routing_stats.get(task_type, {})
        best_worker = max(stats, key=stats.get) if stats else "data_agent"
        return best_worker
    
    async def execute_and_track(self, worker, task):
        try:
            result = await worker.process_async(task)
            # Update success rate
            self.routing_stats[task_type][worker.name] += 0.1
            return result
        except Exception:
            self.routing_stats[task_type][worker.name] -= 0.2
            raise
Chép
Hướng 6e: Implement Real-time Monitoring Dashboard
Idea: Web dashboard hiển thị system metrics real-time.

Cài đặt:

# Create web dashboard
code scripts/dashboard.py
Chép
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/metrics")
async def get_metrics():
    return {
        "active_requests": system.active_task_count(),
        "coordinator_load": system.coordinator.queue_size(),
        "worker_status": {
            "data_agent": "idle",
            "code_agent": "processing",
            "evaluator": "idle"
        },
        "latency_p50": 1.5,
        "latency_p99": 7.3,
        "error_rate": 0.5
    }

@app.get("/logs")
async def get_logs(limit: int = 100):
    return system.message_queue.get_message_log()[-limit:]
Chép
Ghi vào báo cáo:

## Phụ lục: 6e - Real-time Monitoring Dashboard

- Built FastAPI web dashboard
- Display metrics: active requests, worker status, latency, error rate
- Live log viewer
- Access at http://localhost:8000/dashboard
Chép
Checklist Báo cáo Phần 6
 Mục 1: Tổng quan bài lab
 Mục 2: Kiến trúc design (sơ đồ + mô tả)
 Mục 3: Implementation details (decisions + trade-offs)
 Mục 4: Test results (15+ tests, all pass)
 Mục 5: Performance analysis (latency, throughput, bottlenecks)
 Mục 6: Error analysis & resilience
 Mục 7: Design vs Implementation comparison
 Mục 8: Scalability analysis
 Mục 9: Limitations & considerations
 Mục 10: Conclusion & next steps
 (Bonus) Chọn 1 hướng 6a-6e + ghi phụ lục
 Commit: git add report/ && git commit -m "part 6: final report"
🎯 TỔNG HỢP - CHECKLIST TOÀN BỘ LAB DAY 20
Phần 0
 Fork + clone repo Day 20
 Setup venv + cài thư viện
 .env + key OpenAI
 Đọc README + LAB_GUIDE
Phần 1
 Vẽ sơ đồ kiến trúc
 Xác định agents + roles
 Define communication protocol
 Trả lời 3 câu → báo cáo mục 1
Phần 2
 Cài Coordinator: parse, route, execute, aggregate
 Error handling: timeout, retry
 Test coordinator (mock workers)
Phần 3
 Cài BaseWorker class
 Cài Data, Code, Evaluator agents
 Cài MessageQueue
 Integration test: coordinator ↔ worker
Phần 4
 Cài QueryDatabaseTool (SQL)
 Cài PythonREPLTool (sandbox)
 Cài CreateFileTool + EditFileTool
 Cài ScoringTool + ValidationTool
 Test tool integration end-to-end
Phần 5
 Viết 23+ test cases (unit + integration + e2e)
 All tests pass
 Run performance benchmark
 Analyze bottlenecks
 Ghi metrics vào báo cáo mục 5-6
Phần 6
 Viết 10 mục báo cáo
 Include: architecture, test results, performance, analysis
 (Bonus) Chọn 1 hướng (6a-6e)
 Push to GitHub
 Submit
Thời gian ước tính: 22-25 giờ
Budget: ~0,10 USD (gpt-4o-mini)
Bonus: +5 điểm (nếu chọn hướng 6a-6e)