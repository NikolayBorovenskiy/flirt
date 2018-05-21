<a href="#" class="chatperson" data-uuid="<%= uuid %>">
    <% for (var i = 0; i < members.length; i++) { %>
        <% if (user.email != members[i].email) { %>
            <span class="chatimg">
                <img src="<%= members[i].avatar %>" alt=""/>
            </span>
            <div class="namechat">
                <div class="pname"><%= members[i].last_name %> <%= members[i].first_name %></div>
                <div class="lastmsg"><%= last_message ? last_message.content : '' %></div>
            </div>
        <% } %>
    <% } %>
</a>
