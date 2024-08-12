import streamlit as st
import oci


# Step 1: Initialize OCI Generative AI Inference Client
def create_chain():
    config = oci.config.from_file('~/.oci/config', 'DEFAULT')
    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
        config=config,
        service_endpoint=endpoint,
        retry_strategy=oci.retry.NoneRetryStrategy(),
        timeout=(10, 240)
    )

    def invoke_chat(user_message):
        chat_request = oci.generative_ai_inference.models.CohereChatRequest()
        chat_request.message = user_message
        chat_request.max_tokens = 600
        chat_request.temperature = 1
        chat_request.frequency_penalty = 0
        chat_request.top_p = 0.75
        chat_request.top_k = 0

        chat_detail = oci.generative_ai_inference.models.ChatDetails()
        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
            model_id="ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyawk6mgunzodenakhkuwxanvt6wo3jcpf72ln52dymk4wq"
        )
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = "ocid1.tenancy.oc1..aaaaaaaa77cvvhxu6a7dauvbzrhxeoamifazsqzl47ygggdhbrjymt2zmu2q"

        chat_response = generative_ai_inference_client.chat(chat_detail)
        return chat_response  # Return the whole chat_response object

    return invoke_chat


# Step 2: Define Streamlit UI
if __name__ == "__main__":
    chain = create_chain()

    st.subheader("Pretius: Chatbot powered by OCI Generative AI Service")
    user_input = st.text_input("Ask me a question")

    if user_input:
        bot_response = chain(user_input)
        if bot_response.status == 200:
            # Ensure bot_response is correctly accessed based on actual structure
            chat_response = bot_response.data.chat_response  # Assuming chat_response is within data attribute
            if chat_response:
                st.write("Question: ", user_input)
                st.write("Answer: ", chat_response.text)  # Adjust based on actual structure
            else:
                st.write("Unexpected response format from OCI Generative AI Service.")
        else:
            st.write("Error communicating with OCI Generative AI Service.")
