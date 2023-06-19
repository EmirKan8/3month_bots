class FSMMentor(StatesGroup):
    name = State()
    direction = State()
    age = State()
    group = State()

async def start_mentor_creation(message: types.Message, state: FSMContext):
    await FSMMentor.name.set()
    await message.answer("Введите имя ментора:")

async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMMentor.next()
    await message.answer("Введите направление менторства:")

async def enter_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMMentor.next()
    await message.answer("Введите возраст ментора:")

async def enter_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await FSMMentor.next()
    await message.answer("Введите группу ментора:")

async def enter_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text