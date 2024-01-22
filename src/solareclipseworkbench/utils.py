COMMANDS = {
    'voice_prompt': voice_prompt,
    'take_picture': take_picture
}
def start_scheduler():
    """ Start background scheduler and return it.

    Returns: Background scheduler that has been started.
    """

    scheduler = BackgroundScheduler()
    scheduler.start()

    return scheduler


def schedule_commands(filename: str, scheduler: BackgroundScheduler, reference_moments):
    """ Schedule commands as specified in the given file.

    Args:
        - filename: Name of the file in which the commands have been listed, scheduled relatively to the given
                    reference moments
        - scheduler: Background scheduler to use to schedule the commands
        - reference_moments: Dictionary with the reference moments (1st - 4th contact and maximum eclipse), with
                             respect to which the commands are scheduled

    Returns: Scheduler that is used to schedule the commands.
    """

    with open(filename, "r") as file:
        for cmd_str in file:
            schedule_command(scheduler, reference_moments, cmd_str)


def schedule_command(scheduler: BackgroundScheduler, reference_moments, cmd_str: str):
    """ Schedule the given command with the given scheduler and reference moments.

    Args:
        - scheduler: Background scheduler to use to schedule the command
        - reference_moments: Dictionary with the reference moments of the solar eclipse, as datetime objects
        - cmd_str: Command string
    """

    cmd_str_split = cmd_str.split(",")
    func_name = cmd_str_split[0].lstrip()
    ref_moment = cmd_str_split[1].lstrip()
    sign = cmd_str_split[2].lstrip()    # + or -
    hours, minutes, seconds = cmd_str_split[3].lstrip().split(":")   # mm:ss.ss
    description = cmd_str_split[-1].lstrip()

    logging.info(f"Scheduling {func_name} at {ref_moment}{sign}{cmd_str_split[3].lstrip()}")

    args = cmd_str_split[4:-1]

    func = COMMANDS[func_name]

    # ref_moment = datetime.now()
    reference_moment = reference_moments[ref_moment]
    delta = timedelta(hours=float(hours), minutes=float(minutes), seconds=float(seconds))

    if sign == "+":
        execution_time = ref_moment + delta
    else:
        execution_time = ref_moment - delta

    trigger = CronTrigger(year=execution_time.year, month=execution_time.month, day=execution_time.day,
                          hour=execution_time.hour, minute=execution_time.minute,
                          second=execution_time.second)

    scheduler.add_job(func, trigger=trigger, args=args, name=description)
