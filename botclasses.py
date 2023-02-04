import bbot, nextcord


class AcceptOrDeny(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.accepted = False

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.green)
    async def acc(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("{} **accepted** their interview".format(interaction.user))
        self.value = True
        self.accepted = True
        self.stop()
    
    @nextcord.ui.button(label="Deny", style=nextcord.ButtonStyle.red)
    async def deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("{} **denied** their interview".format(interaction.user))
        self.value = True
        self.stop()

class Applications(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Staff Application",
            timeout=5 * 60,  # 5 minutes
        )

        self.shoe = nextcord.ui.TextInput(
            label="What shoe would you be?",
            min_length=1,
            max_length=50,
        )
        self.add_item(self.shoe)

        self.description = nextcord.ui.TextInput(
            label="Why should we hire you",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Speak professionally & show experience",
            required=False,
            max_length=1800,
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message("Your staff application was sent to staff to be reviewed. You will be DMed your results.",ephemeral=True)

        embed = nextcord.Embed(title='{} applied for staff'.format(interaction.user))
        embed.add_field(name='If you could be a shoe, what shoe would you be?', value="`{}`".format(self.shoe.value), inline=True)
        embed.add_field(name='Why should we hire you??', value="`{}`".format(self.description.value), inline=True)

        view = AcceptOrDeny()
        channel = bbot.bot.get_channel(1071392140036427846)
        await channel.send(embed=embed,view=view)
        await view.wait()
        
        if view.value:
            if view.accepted:
                embed = nextcord.Embed(title='Interview status',description='''After careful consideration, we have decided that your interiew would be **Accepted**. Congratulations!
                We look forward to your work, make sure not to slack off >:)
                ''')
                await interaction.user.send(embed=embed)
            else:
                embed = nextcord.Embed(title='Interview status',description='''After careful consideration, we have decided that your interiew would be **Declined**. Sorry!
                We look forward to your next interview, maybe we will see you in the near future! :)
                ''')
                await interaction.user.send(embed=embed)

        
